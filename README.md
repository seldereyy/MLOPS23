Чтобы запустить сервер, введите
`poetry run start`
После этого доступен swagger по:
http://127.0.0.1:5049/docs

Немного косякнула с poetry. Весь проект живет в директории src. 
В папке src две ключевые папки:
* `ml_ops_1` - root папка проекта. В ней лежит main и utils, конфиг для инициализации папки хранения моделей и названия типов моделей
* `models` - обертки на 2 модели: LogisticRegression sklearn и XGBClassifier реализации xgboost. Над ними класс BasicWrapper, инцииализирующий основные методы и абстрактные, различные для моделей

Не разобралась с ошибками, вывожу просто текстом. Понимаю, что так не пойдет, надо исправлять...

В папке tests:
* test_data - пример данных, на которых тестила работу сервера (базово sklearn make_blobs на 3 класса и разделение на train test)
* test, train - json файлы для формирования запросов в сервер

В папке models_data результаты экспериментов работы с сервером - обученные модели

У сервера несколько методов. Реализация обновления модели по имени файла - удаляем, если такой уже существует и обучаем заново. Предполагался видимо put, не успела.
* `list_models` - метод GET, возвращает список типов моделей, доступных для обучения. Пример запроса CLI:
```
curl -X 'GET' \
  'http://127.0.0.1:5049/list_models' \
  -H 'accept: application/json'
* ``
```

* `delete_model` - метод DELETE, удаляет пикл с обученной моделью из папки с моделями. Пример запроса CLI:
```
curl -X 'DELETE' \
  'http://127.0.0.1:5049/delete_model?filename=test1' \
  -H 'accept: application/json'
```

* `train_model` - метод POST, обучает модель. На вход нужны имя будущего файла, тип модели из предложенных, данные для обучения в формате json (X_train и y_train). Пример запроса CLI:
  ```
  curl -X 'POST' \
  'http://127.0.0.1:5049/train_model?filename=f1&model_type=MyLogisticRegression' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "X_train": [
    [
      1,2,3,
    ],
    [
      3,4,5,
    ]
  ],
  "y_train": [
    0,1,0
  ],
  "params": {}
}'
  ```

* `get_preds` - метод POST для предсказания обученной моделью. На вход нужно имя файла обученной модели. Возвращает предикты в виде листа. Пример запроса CLI:

```
curl -X 'POST' \
  'http://127.0.0.1:5049/get_preds?filename=logreg.pkl' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "X_test": [
    [1,2,3]
  ]}'
```
