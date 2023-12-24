from minio import Minio
import pickle
import io
from fastapi import HTTPException

MINIO_HOST = 'localhost'
MINIO_ACCESS_KEY = 'admin'
MINIO_SECRET_KEY = 'admin1234'


class MINIO_DVC:
    def __init__(self):  # endpoint: str, access_key: str, secret_key: str
        self.url = f"http://{MINIO_HOST}:9000"
        self.access_key = MINIO_ACCESS_KEY
        self.secret_key = MINIO_SECRET_KEY
        self.minio_client = Minio(
            f"{MINIO_HOST}:9000",
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )

    def check_exists(self, model_name, bucket_name):
        if model_name[-4:] != ".pkl":
            model_name += ".pkl"
        files=self.minio_client.list_objects(bucket_name)
        return model_name in [f.object_name for f in files]

    def save_model(self, model_name, model, bucket_name='models'):
        buckets = [x.name for x in self.minio_client.list_buckets()]

        if bucket_name not in buckets:
            self.minio_client.create_bucket(Bucket=bucket_name)
        bytes_file = pickle.dumps(model)
        if model_name[-4:] != ".pkl":
            model_name += ".pkl"
        self.minio_client.put_object(
                bucket_name=bucket_name,
                object_name=f"{model_name}",
                data=io.BytesIO(bytes_file),
                length=len(bytes_file),
            )

    def load_model(self, model_name):
        
        if self.check_exists(model_name, 'models'):
            self.minio_client.fget_object(
                bucket_name="models", object_name=model_name + ".pkl", file_path=f"./models_data/{model_name}.pkl"
            )
            with open(f"./models_data/{model_name}.pkl", "rb") as f:
                model=pickle.load(f)

            return model
        else:
            raise HTTPException(status_code=404, detail="Такая модель не была обучена")
    
    def delete_model(self, model_name):
        self.minio_client.remove_object(bucket_name="models", object_name=model_name + ".pkl")
    