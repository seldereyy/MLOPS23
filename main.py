import os
import json
import numpy as np
import pandas as pd

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile

from src.save_load import MINIO_DVC

from src.models import  MyLogisticModel
from src.models  import MyXGBoost  

MINIO_DVC=MINIO_DVC()
app = FastAPI()
model_types = MyLogisticModel.MyLogisticRegression().list_models()
map_types_models = {
    "MyLogisticRegression": MyLogisticModel.MyLogisticRegression,
    "MyXGBoost": MyXGBoost.MyXGBoost,
}

@app.get("/list_models", status_code=200)
def list_available_models():
    """
    Метод, который возвращает список доступных для обучения моделей
    """
    return model_types

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
    X_train.index= range(len(X_train))
    # X_train=[]
    # for feat in X_train_.values():
    #     X_train.append(feat)
    y_train= pd.DataFrame(json.load(y_train.file))
    # return X_train[:10]

    if not model_type in model_types:
        "Тест на адекватность запроса"
        raise HTTPException(status_code=404, detail="Такой тип модели я не прописывала") 

    if MINIO_DVC.check_exists(model_name=filename, bucket_name="models"):
        "Переобучим модель, если она уже была обучена"
        MINIO_DVC.delete_model(filename)
        # delete_model(filename)

    try:
        model = map_types_models[model_type](**{})
        model.fit(X_train, y_train)
        MINIO_DVC.save_model(filename, model)
        return 'Success!'
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    

@app.post("/get_preds", status_code=200)
def model_predict(filename: str, X_test: UploadFile,):
    """
    Получаем предсказания модели в виде листа 
    """
    X_test= pd.DataFrame(json.load(X_test.file))
    model=MINIO_DVC.load_model(filename)

    return model.predict(X_test).tolist()

@app.delete("/delete_model", status_code=200)
def delete_model(filename: str):
    """
    Удаляет модель по заданному имени файла в папке.\\
    filename - имя файла, который нужно удалить\\

    return: информация об успешном удалении файла
    """
    if MINIO_DVC.check_exists(model_name=filename, bucket_name="models"):
        MINIO_DVC.delete_model(filename)
        return f'File {filename} was removed'
    else:
        raise HTTPException(status_code=404, detail="Такая модель не была обучена")

def start():
    """
    Чтобы собрать приложение, просто: `poetry run start` at root level
    Взяла отсюда: https://stackoverflow.com/questions/63809553/how-to-run-fastapi-application-from-poetry 
    """
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
