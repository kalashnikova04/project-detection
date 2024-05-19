<!-- Версия в kubernetes -->

## Запуск проекта

1. Не забудьте включить Docker Desktop или запустить docker через terminal.
2. В терминале:

    1. Клонируйте репозиторий 
    ```git clone -b version-k8s https://github.com/kalashnikova04/project-detection.git project-detection-v-k8s```
    2. ```cd project-detection-v-k8s```
    3. `minikube start`
    4. `kubectl create namespace lpdet`, переключитесь на namespace lpdet в своем IDE.
    5. ```kubectl -n lpdet apply -Rf kubernetes/```
    6. ```minikube tunnel```
    7. `minikube addons enable ingress`
3. В файл `/etc/hosts (C:/Windows/System32/drivers/etc/hosts)`, запущенный с правами администратора, добавьте 2 строки (если работаете через WSL):
    - `127.0.0.1 license-plate-detection.ru`
    - `127.0.0.1 rabbitmq.license-plate-detection.ru`
4. Дождитесь пока все поды *lpdet* и *ingress-nginx* будут в статусе Running (`kubectl get pod --all-namespaces`).
5. В браузере перейдите по адресу https://license-plate-detection.ru/ для работы с основным сайтом.

## Функционал сервиса

На всех страницах сервиса в заголовке есть панель навигации. Всего 4 раздела:
- Upload - перенаправляет в корневой каталог
- Train - `href="/train/"`
- See Tasks - `href="/task_status/"`
- Inference - `href="/inference/"`

Рассмотрим каждый раздел отдельно:

https://license-plate-detection.ru/ - форма для загрузки изображений. После нажатия кнопки ```Upload``` загруженные изображения появятся на экране. Чтобы перейти к следующему этапу нажмите на кнопку ```Get preds```, которая перенаправит запрос в раздел ```model_mode/```

https://license-plate-detection.ru/model_mode/ - промежуточная страница, которая информирует переведена ли модель в режим обучения или инференса. Нажав на ```status```, вы перейдете в раздел ```task_status/```

https://license-plate-detection.ru/task_status/ - страница для просмотра статуса задач из очереди, в нашем случае задач обучения и инференса.

https://license-plate-detection.ru/inference/ - страница для просмотра детектированных объектов на загруженных изображениях.

https://license-plate-detection.ru/train/ - тренировка модели Yolov8.

https://license-plate-detection.ru/admin/ - админ-панель для суперпользователя, данные которого заданы в ConfigMap django.

https://rabbitmq.license-plate-detection.ru/ - UI сервиса RabbitMQ, данные для входа заданы в ConfigMap rmq.