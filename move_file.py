from google.cloud import storage
import boto3
import io

gcp_bucket = ''
aws_bucket = ''

client = storage.Client()
bucket = client.get_bucket(gcp_bucket)
# obviously don't hard code a filename
filename = ''
blob = bucket.get_blob(filename)
# there could be a better solution than loading this into memory
data = io.BytesIO()
blob.download_to_file(data)
data.seek(0)

s3 = boto3.client("s3")
s3.upload_fileobj(data, aws_bucket, filename)
