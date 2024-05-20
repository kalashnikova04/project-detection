import json
import os

import pika
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from main.models import LicensePlate, Task

from .forms import ImageForm

RMQ_URL = os.getenv("RMQ_URL")
QUEUE_NAME = os.environ.get("QUEUE_NAME", "test_direct")
EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME", "to_direct")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


def index(request):
    if request.method == "POST":
        form = ImageForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            ids = []
            for image in files:
                lp = LicensePlate.objects.create(title=image.name, image=image)
                ids.append(lp.id)
            messages.success(request, "Images added")
            return render(
                request,
                "main/index.html",
                {"form": form, "images": LicensePlate.objects.filter(id__in=ids)},
            )

        return render(request, "main/index.html", {"form": form})

    else:
        form = ImageForm()
    return render(request, "main/index.html", {"form": form})


def train_yolo(request):
    pass


def send_inference_task(request):
    try:
        recieved_data = request.GET.dict()
    except Exception as e:
        print(e)
        return render(request, "main/error.html")

    routing_key = ""
    worker_id = "Unknown"

    images = []
    for k in recieved_data.keys():
        if k == "csrfmiddlewaretoken":
            continue
        images.append(recieved_data[k])
    request.session["images"] = images

    with pika.BlockingConnection(pika.URLParameters(RMQ_URL)) as connection:
        with connection.channel() as channel:

            task = Task(status="PENDING", worker_id=worker_id, mode="inference")
            task.save()
            task_num = task.id
            data = {"images": images, "task_id": task_num}

            channel.exchange_declare(
                exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True
            )
            channel.queue_declare(queue=f"{QUEUE_NAME}_rejected", durable=True)
            channel.queue_declare(
                queue=QUEUE_NAME,
                durable=True,
                arguments={
                    "x-dead-letter-exchange": "",
                    "x-dead-letter-routing-key": f"{QUEUE_NAME}_rejected",
                },
            )
            channel.queue_bind(
                queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key="direct_out"
            )

            channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key=routing_key,
                body=json.dumps(data, cls=DjangoJSONEncoder).encode(),
            )

    context = {"task_num": task_num, "mode": "inference"}

    return render(request, "main/mode.html", context)


async def update_task_status(request):
    print("[update_task_status]")
    tasks = [task async for task in Task.objects.all()]
    context = {"tasks": tasks}
    return render(request, "main/tasks.html", context)


def get_prediction(request):
    images = request.session.get("images")
    context = {"images": images}
    return render(request, "main/get_predicted.html", context)
