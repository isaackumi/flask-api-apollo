import boto3
from dotenv import load_dotenv
import os
import io

# Load environment variables from .env file
load_dotenv()

def store_csv_in_s3(bucket_name, file_name,file_content):
    """
    Store a CSV file in an S3 bucket and return the URL.

    :param bucket_name: The name of the S3 bucket.
    :param file_name: The name of the file to store.
    :param file_content: The contents of the file to store.
    :return: The URL of the stored file.
    """
    # Create an S3 client with your AWS access key and secret key
    s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

    # Check if the bucket exists and create it if necessary
    if not bucket_exists(bucket_name):
        s3.create_bucket(Bucket=bucket_name)

    # Create a file-like object from the string content
    file_obj = io.StringIO(file_content)

    # Upload the file to S3
    s3.upload_file(file_obj, bucket_name, file_name)

    # Set the object ACL to public-read
    s3.put_object_acl(ACL='public-read', Bucket=bucket_name, Key=file_name)

    # Generate the URL for the file
    url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"

    # Return the URL
    return url

def bucket_exists(bucket_name):
    """
    Check if an S3 bucket exists.

    :param bucket_name: The name of the S3 bucket to check.
    :return: True if the bucket exists, False otherwise.
    """
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        return True
    except:
        return False
