import boto3

from portaljob.config import settings

_s3_client = boto3.client(
    "s3",
    endpoint_url=settings.minio_endpoint_url,
    aws_access_key_id=settings.minio_access_key,
    aws_secret_access_key=settings.minio_secret_key,
)


def upload_raw_content(storage_key: str, content: str, content_type: str) -> None:
    _s3_client.put_object(
        Bucket=settings.minio_bucket_raw,
        Key=storage_key,
        Body=content.encode("utf-8"),
        ContentType=content_type,
    )
