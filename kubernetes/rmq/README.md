## RabbitMQ

Сервис обеспечивает коммуникацию между producer (web) и consumer (models) с помощью очереди сообщений.

В Kubernetes rmq состоит из ConfigMap, StatefulSet, 2 Services, Role for peer-discovery. Открыто 2 порта: 5672 для внутрисетевого взаимодействия между сервисом web и models по amqp-url и 15672 для UI RabbitMQ.
