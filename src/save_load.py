from minio import Minio
import pickle
from io import BytesIO
from s3.dvc_data import DVC

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
        self.dvc = DVC(self.url, self.access_key, self.secret_key)

    def save_data(self, data):
        self.dvc.data_versionise(data)

    def save_model(self, model_name, model, bucket_name='models'):
        buckets = [x["Name"] for x in self.minio_client.list_buckets()["Buckets"]]

        if bucket_name not in buckets:
            self.minio_client.create_bucket(Bucket=bucket_name)

        with BytesIO() as f:
            pickle.dump(model, f)
            f.seek(0)
            self.minio_client.upload_fileobj(
                Bucket=bucket_name, Key=model_name + ".pkl", Fileobj=f
            )

    def load_model(self, model_name):
        self.minio_client.download_file(
            Bucket="models", Key=model_name + ".pkl", Filename=model_name + ".pkl"
        )
        with open(f"{model_name}.pkl", "rb") as f:
            model=pickle.load(f)

        return model

    def delete_model(self, model_name):
        self.minio_client.delete_object(Bucket="models", Key=model_name + ".pkl")

