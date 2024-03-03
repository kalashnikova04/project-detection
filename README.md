# Детекция номеров объектов методами глубинного обучения

***Автор работы:*** Калашникова Анастасия ([telegram](https://t.me/kalassnikovaa))

***Научный руководитель:*** Гаврилова Елизавета ([telegram](https://t.me/lizvladii))

## Постановка задачи:

Создать сервис с обученной нейронной сетью для детекции российских номеров автомобилей на изображении.

## План выполнения проекта:
<table>
    <thead>
        <tr>
            <th>Часть проекта</th>
            <th>Название</th>
            <th>Срок выполнения</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center">Данные</td>
            <td align="center">Выбрать существующий датасет</td>
            <td align="center">06.03.24</td>
        </tr>
        <tr>
            <td rowspan=2 align="center">DL</td>
            <td align="center">Провести эксперименты по обучению YOLOv5 / mmdetection  на датасете</td>
            <td align="center">08.04.24</td>
        </tr>
        <tr>
            <td align="center">Инференс</td>
            <td align="center">12.04.24</td>
        </tr>
        <tr>
            <td rowspan=7 align="center">Сервис</td>
            <td align="center">Организация кода по файлам, pre-commit</td>
            <td align="center">13.04.24</td>
        </tr>
        <tr>
            <td align="center">Хранение и управление данными (dvc)</td>
            <td align="center">14.04.24</td>
        </tr>
        <tr>
            <td align="center">ТГ-бот</td>
            <td align="center">17.04.24</td>
        </tr>
        <tr>
            <td align="center">Тестирование</td>
            <td align="center">21.04.24</td>
        </tr>
        <tr>
            <td align="center">Логирование</td>
            <td align="center">23.04.24</td>
        </tr>
        <tr>
            <td align="center">CI&CD</td>
            <td align="center">26.04.24</td>
        </tr>
        <tr>
            <td align="center">Мониторинг</td>
            <td align="center">01.05.24</td>
        </tr>
    </tbody>
</table>

## Описание проекта:

Конечная версия - телеграм-бот, позволяющий по загруженному изображению детектировать области с номерами машин (выдавать координаты окошка с номерами либо возвращать загруженное изображение с выделенной областью), на основе методов глубинного обучения (DL).

Стек: Python, AirFlow, Docker, PostgreSQL

Внутри бота планируется простой функционал для получения изображения с детектированным объектом. Команды:

- /start - начать работу с ботом;
- /upload_image - загрузить изображение для детекции - через некоторое время бот отдает обновленное изображение.

Возможно, будет добавлена команда для загрузки нескольких изображений.


## Примечания:
Описала **примерно**, тк работу над дипломом еще не начинала.
