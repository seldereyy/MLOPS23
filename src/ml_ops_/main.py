import os
import pickle
import sys
from urllib.error import HTTPError

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from src.ml_ops_1.utils import load_yaml, pickle_dump, pickle_load

sys.path.append("/Users/user/HSE/ml_ops/src/models/")

import MyLogisticModel
import MyXGBoost  

map_types_models = {
    "MyLogisticRegression": MyLogisticModel.MyLogisticRegression,
    "MyXGBoost": MyXGBoost.MyXGBoost,
}

config = load_yaml("/Users/user/HSE/ml_ops/src/ml_ops_1/cnf.yml")

app = FastAPI()
class MyAppException(Exception):
    
    def __init__(self, message):
        self.message = message
    def __str(self):
        return self.message

class TrainData(BaseModel):
    X_train: list[list]
    y_train: list
    params: dict = {}


class TestData(BaseModel):
    X_test: list[list]


@app.get("/list_models")
def list_available_models():
    """
    Метод, который возвращает список доступных для обучения моделей
    """
    return config["available_models"]


@app.delete("/delete_model")
def delete_model(filename: str):
    """
    Удаляет модель по заданному имени файла в папке.
    filename - имя файла, который нужно удалить

    return: информация об успешном удалении файла
    """
    if filename[-4:] != ".pkl":
        filename += ".pkl"
    path = os.path.join(config["path_to_models"], filename)

    if os.path.exists(path):
        os.remove(path)
        return f'File {filename} was removed'
    else:
        return "Такая модель не была обучена"


@app.post("/train_model")
def train_model(filename: str, model_type: str, TrainPool: TrainData):
    """
    Обучаем модель  
    filename - имя файла, в который запишется пикл обученной модели в папке для хранения данных
    model_type - тип модели из списка в конфиге. Неправильный тип модели выдает кастомную ошибку
    TrainPool - данные в формате json

    return: Success в случае успеха, пишет пикл модели
    """
    if not model_type in config["available_models"]:
        "Тест на адекватность запроса"
        
        return "Такой тип модели я не прописывала"

    if filename[-4:] != ".pkl":
        filename += ".pkl"

    if os.path.exists(os.path.join(config["path_to_models"], filename)):
        "Переобучим модель, если она уже была обучена"
        print("Delete model")
        delete_model(filename)

    try:
        model = map_types_models[model_type](**TrainPool.params)
        print("Fit model...")
        model.fit(TrainPool.X_train, TrainPool.y_train)
        model.dump(filename)
        return "Success! Model was dumped", 200
    except Exception as e:
        return f'{e}'
    


@app.post("/get_preds")
def model_predict(filename: str, TestPool: TestData):
    """
    Получаем предсказания модели в виде листа 
    """
    path = os.path.join(config["path_to_models"], filename)
    if filename[-4:]!='.pkl':
        filename+='.pkl'
    if not os.path.exists(path):
        return f"Такая модель не была обучена, {path}"
    model = pickle_load(path)

    return model.predict(TestPool.X_test).tolist()


def start():
    """
    Чтобы собрать приложение, просто: `poetry run start` at root level
    Взяла отсюда: https://stackoverflow.com/questions/63809553/how-to-run-fastapi-application-from-poetry 
    """
    uvicorn.run("ml_ops_1.main:app", host="127.0.0.1", port=5049, reload=True)
