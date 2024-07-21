## Задача
Разработать приложение для обработки JSON документов пользователя, схема которых также пользователем и предоставляется разработчикам заранее.

## Основные компоненты
1. CLI приложение для генерации pydantic моделей на основе JSON Schema.
2. CLI приложение для генерации контроллеров REST приложения.
3. REST приложение.
4. База данных.
5. Брокер сообщений Kafka.
6. Спек файлы для запуска приложения в kubernetes кластере.
7. Диаграмма flowchart, описывающая контроллер.

## CLI приложение gen_models
Генерирует pydantic модель и сохраняет в /src/rest/models/engine, файл будет называться Engine.py, если kind = 'engine'
Команда для генерации: gen_models --json-schema=../../engine-schema.json --out-dir=../rest/models/engine

## CLI приложение gen_rest
Генерирует контроллеры для REST приложения и сохраняет их в /src/rest/routes/engine, файл будет называться {Название pydantic модели}_controller.py
Команда для генерации: gen_rest --models-../rest/models/engine --rest-routes=../rest/routes/engine

## База данных
В models.py описан класс DocumentORM, сессия и функция для создания таблиц.
В DocumentRepository.py описан класс с методами для взаимодействия с базой данных.

## REST приложение
GET: /{kind}/{uuid}/state - возвращение значения статуса объекта<br/>
GET: /{kind}/{uuid} - возвращение объекта из базы данных<br/>
POST: /{kind}/ - запрос на сохранение json документа<br/>
PUT: /{kind}/{uuid}/configuration/ - изменение значения словаря specification<br/>
PUT: /{kind}/{uuid}/settings/ - изменение значения словаря settings<br/>
PUT: /{kind}/{uuid}/state - изменение значения статуса объекта<br/>
DELETE: /{kind}/{uuid}/ - удаление объекта из базы данных<br/>

## Спек файлы
Предложены спек файлы для запуска приложения в kubernetes кластере. Создал образ приложения на hub.docker.com в daviddz27/k8s-json-app
