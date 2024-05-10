import os
from django.shortcuts import render
from .forms import ImageForm
from media.back_model_dino4_inference import backend_model_inference 


def index(request):
    # if os.path.exists('model.pickle') and os.path.exists('data.npz'):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img = form.instance
            context = {'form': form, 'img': img, 'img_title': img.image.url[15:]}
            return render(request, 'main/index.html', context=context)
    else:
        form = ImageForm()
        return render(request, 'main/index.html', {'form': form})
    # return render(request, 'main/need_train.html')


def train_yolo(request):
    return


def get_prediction(request):
    try:
        img = request.FILES.get('image')
        # print(img, img.size, img.name, img.field_name)
    except Exception as e:
        print(e)
        return render(request, 'main/error.html')

    images = [img]

    backend_model_inference(image=img)
    print(img)

    context = {'images': [img.name]}
    return render(request, 'main/get_predicted.html', context)
