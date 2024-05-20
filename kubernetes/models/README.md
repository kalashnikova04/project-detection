## Models

Сервис основан на двух библиотеках: MMDetection и MMDeploy. На основе первой проводились эксперименты с обучением моделей, с помощью второй обученная модель была развернута на ONNXRuntime для инференса на CPU.

Описание составляющих сервиса можно посмотреть на ветке master [mmdet/README.md](https://github.com/kalashnikova04/project-detection/blob/master/mmdet/README.md)

Подключенные хранилища (persistent volumes):
- pv-media - для инференса на изображениях, загруженных пользователем;
- pv-models - для хранения чекпоинта выбранной модели.

Для скачивания builded image выполните команду: `docker pull kalashnikova/lp-detection:mmdeploy_2`
