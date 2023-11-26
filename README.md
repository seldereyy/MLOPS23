Чтобы запустить сервер, введите
`poetry run start` \
После этого доступен swagger по: \
http://127.0.0.1:5000/docs \
Мой тг: @selderey17

В папке `./src/` лежит:
* `./cnf.yml` - небольшой конфиг с базовыми путями и названиями моделей;
* `./models/` - обертки на 2 модели: LogisticRegression sklearn и XGBClassifier реализации xgboost. Над ними класс BasicWrapper, инцииализирующий основные методы и абстрактные, различные для моделей;
* `./pickle_utils.py` - небольшой файлик с обработкой пиклов и загрузкой ямлов.

В папке `./tests/`:
* `test_data.ipynb` - пример данных, на которых тестила работу сервера (базово sklearn make_blobs на 3 класса и разделение на train test)
* `test.json`, `train.json` - json файлы для формирования запросов в сервер, можно кидать их в swagger

В папке `./models_data/` результаты экспериментов работы с сервером - обученные модели


Сервер возвращает следующие status_code:
* 200, 201 - при успешном выполнении методов (201 для train)
* 404 в случае, если введен неправильный тип модели или неверное название файлика (нет в списке обученных моделей для инференса, удаления)
* 400 - в случае неправильно указанных параметров обучения модели, выводится текст ошибки от python

У сервера несколько методов: 
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
  "params": { }'
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
