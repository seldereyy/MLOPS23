import os
import json

import pandas as pd

import uvicorn
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel

# from src.pickle_utils import load_yaml, pickle_load
# from src.minio_utils import put_model
from src.save_load import MINIO_DVC

from src.models import  MyLogisticModel
from src.models  import MyXGBoost  

map_types_models = {
    "MyLogisticRegression": MyLogisticModel.MyLogisticRegression,
    "MyXGBoost": MyXGBoost.MyXGBoost,
}

config = load_yaml("src/cnf.yml")

app = FastAPI()

class TrainData(BaseModel):
    # X_train: list[list]
    # y_train: list
    params: dict = {}


# class TestData(BaseModel):
#     X_test: list[list]

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}

@app.get("/list_models", status_code=200)
def list_available_models():
    """
    Метод, который возвращает список доступных для обучения моделей
    """
    return config["available_models"]

@app.post("/train_model", status_code=201)
def train_model(filename: str, model_type: str, X_train: UploadFile, y_train: UploadFile):#, TrainPool: TrainData):
    """
    Обучаем модель  \\
    filename - имя файла, в который запишется пикл обученной модели в папке для хранения данных \\
    model_type - тип модели из списка в конфиге. Неправильный тип модели выдает кастомную ошибку\\
    TrainPool - данные в формате json\\

    return: Success в случае успеха, пишет пикл модели
    """
    X_train= pd.DataFrame(json.load(X_train.file))
    y_train= pd.DataFrame(json.load(y_train.file))

    if not model_type in config["available_models"]:
        "Тест на адекватность запроса"
        
        raise HTTPException(status_code=404, detail="Такой тип модели я не прописывала") 

    if filename[-4:] != ".pkl":
        filename += ".pkl"

    if os.path.exists(os.path.join(config["path_to_models"], filename)):
        "Переобучим модель, если она уже была обучена"
        MINIO_DVC.delete_model(filename)
        # delete_model(filename)

    try:
        model = map_types_models[model_type](**{})#TrainPool.params)
        print("Fit model...")
        model.fit(X_train, y_train)
        # model.dump(filename)
        return put_model(model, filename, model_type, {})
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    

@app.post("/get_preds", status_code=200)
def model_predict(filename: str, X_test: UploadFile,):
    """
    Получаем предсказания модели в виде листа 
    """
    X_test= pd.DataFrame(json.load(X_test.file))
    path = os.path.join(config["path_to_models"], filename)
    if path[-4:]!='.pkl':
        path+='.pkl'
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Такая модель не была обучена")
    model = pickle_load(path)

    return model.predict(X_test).tolist()

@app.delete("/delete_model", status_code=200)
def delete_model(filename: str):
    """
    Удаляет модель по заданному имени файла в папке.\\
    filename - имя файла, который нужно удалить\\

    return: информация об успешном удалении файла
    """
    if filename[-4:] != ".pkl":
        filename += ".pkl"
    path = os.path.join(config["path_to_models"], filename)

    if os.path.exists(path):
        os.remove(path)
        return f'File {filename} was removed'
    else:
        raise HTTPException(status_code=404, detail="Такая модель не была обучена")


def start():
    """
    Чтобы собрать приложение, просто: `poetry run start` at root level
    Взяла отсюда: https://stackoverflow.com/questions/63809553/how-to-run-fastapi-application-from-poetry 
    """
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
