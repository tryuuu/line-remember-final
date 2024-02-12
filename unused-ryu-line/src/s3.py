import boto3
import uuid
def upload_to_s3(image_data, user_id):
    """
    S3に画像をアップロードし、画像のURLを返します。

    :param image_data: アップロードする画像データ
    :param user_id: ユーザーID（S3のパスに使用）
    :return: アップロードされた画像のURL
    """
    s3_client = boto3.client('s3')
    bucket_name = 'line-knowledge-ryu'  
    image_key = f"{user_id}/{uuid.uuid4()}.jpg"

    # S3に画像をアップロード
    s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image_data)

    image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_key}"
    return image_url