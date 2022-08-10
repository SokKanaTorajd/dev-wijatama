from google.cloud import storage
from google.oauth2 import service_account
from app import config

credentials_content = {
    'type': 'service_account',
    'project_id': config.GCP_PROJECT_ID,
    'private_key_id': config.GCP_KEY_ID,
    'private_key': config.GCP_KEY,
    'client_email': config.GCP_CLIENT_EMAIL,
    'client-id': config.GCP_CLIENT_ID,
    'auth_uri': config.GCP_AUTH_URI,
    'token_uri': config.GCP_TOKEN_URI,
    'auth_provider_x509_cert_url': config.GCP_AUTH_PROVIDER_CERT_URL,
    'client_x509_cert_url': config.GCP_CLIENT_CERT_URL
}

credentials = service_account.Credentials.from_service_account_file(credentials_content)

storage_client = storage.Client(credentials=credentials)

def upload_blob(source_file_name, destination_blob_name, bucket_name=config.GCP_BUCKET_NAME):
    """Uploads a file to the bucket."""
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))
        return True
    except:
        return False

def download_blob(source_blob_name, destination_file_name, bucket_name=config.GCP_BUCKET_NAME):
    """Downloads a blob from the bucket."""
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_name)

        print('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))
        return True
    except:
        return False

def list_blobs(parent="", bucket_name = "checkma"):
    """Lists all the blobs in the bucket."""
    try:
        # Note: Client.list_blobs requires at least package version 1.17.0.
        blobs = storage_client.list_blobs(bucket_name, prefix=parent)
        listData = []
        for blob in blobs:
            listData.append(blob.name.replace(parent, ""))
        return listData
    except:
        return False

def create_folder(path, bucket_name = "checkma"):
    """ Create a new folder """
    try:
        bucket = storage_client.get_bucket(bucket_name)
        if path[-1] != "/":
            path += "/"
        blob = bucket.blob(path)

        blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
        return True
    except:
        return False

def check_folder_exists(folderPath, bucket_name="checkma"):
    """ check if path/file exists in bucket or not in google storage """
    bucket = storage_client.bucket(bucket_name)
    stats = storage.Blob(bucket=bucket, name=folderPath).exists(storage_client)
    return stats
