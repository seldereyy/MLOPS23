from minio import Minio
import pickle 
import io

MINIO_HOST = 'localhost'
MINIO_ACCESS_KEY = 'admin'
MINIO_SECRET_KEY = 'admin1234'


minio_client = Minio(
    f"{MINIO_HOST}:9000",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def put_model(data, filename: str, model_type: str, params:dict):

    if filename[-4:] != ".pkl":
        folder_name=filename
        filename += ".pkl"
    else:
        folder_name=filename[:-4]

    bytes_file = pickle.dumps(data)

    result = minio_client.put_object(
            bucket_name=model_type.lower(),
            object_name=f"{folder_name}/{filename}",
            data=io.BytesIO(bytes_file),
            length=len(bytes_file),
            metadata={'params': f'{params}', 'model_type': model_type}
        )

    return  f'created {result.object_name} object; etag: {result.etag}, version-id: {result.version_id}'

