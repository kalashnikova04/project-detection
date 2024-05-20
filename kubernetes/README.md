## Описание сервиса

**Разделы:**
- *db* - [db/README.md](https://github.com/kalashnikova04/project-detection/tree/version-k8s/kubernetes/db/README.md)
- *models* - [models/README.md](https://github.com/kalashnikova04/project-detection/tree/version-k8s/kubernetes/models/README.md)
- *rmq* - [rmq/README.md](https://github.com/kalashnikova04/project-detection/tree/version-k8s/kubernetes/rmq/README.md)
- *web* - [web/README.md](https://github.com/kalashnikova04/project-detection/tree/version-k8s/kubernetes/web/README.md)
- *volumes* - содержит 3 Persistent Volumes, 3 Persisent Volume Claims и аккаунт с открытым доступом к volumes.
- *ingress* - ingress типа nginx.

    Содержит 2 хоста:
    1. `license-plate-detection.ru`

        В случае запроса статики или изображений, загруженных пользователем, перенаправляет на сервис static-svc (nginx) из раздела web. В случае запросов на взаимодействие с приложением, перенаправляет их на сервис django-svc из раздела web.
    2. `rabbitmq.license-plate-detection.ru`

        Все запросы перенаправляет на сервис внешний сервис rabbitmq (порт 15672) из раздела rmq.
