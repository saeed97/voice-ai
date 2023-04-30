from requests import Response
from .s3_config import config
import boto3
import os
from botocore.exceptions import NoCredentialsError
import logging

log = logging.getLogger(__name__)

class S3:
    def __init__(self) -> None:
        self.s3 = boto3.client('s3', aws_access_key_id=config.S3_ACCESS_KEY, aws_secret_access_key=config.S3_SECRET_KEY, region_name=config.S3_REGION)


    def save_audioFile_to_bucket(self, audio_output, file_path) -> bool:
        try:
            self.s3.put_object(Body=audio_output.audio_data, Bucket=config.S3_BUCKET, Key=f"{file_path}")
            return {"status": "success", "path": file_path}, 200
        except NoCredentialsError:
            return {"status": "Failed"}, 500
    
    def saveText_to_aws(self, text, file_path) -> bool:
        try:
            self.s3.put_object(Body=text, Bucket=config.S3_BUCKET, Key=f"{file_path}")
            return {"status": "success", "path": file_path}, 200
        except NoCredentialsError:
            return {"status": "Failed"}, 500
    
    def get_audio_stream(self, audio_path):
        try:
            s3_object = self.s3.get_object(Bucket=config.S3_BUCKET, Key=f"{audio_path}")
            return s3_object.get('Body'), 200, audio_path
        except Exception as e:
            log.error("Error: unhandled error occured during stream audio!!")
            return {"status": "Fail", "message": "error during processing the audio!!"}, 500, audio_path
    
    def fetch_text_file(self, file_path):
        s3_object = self.s3.get_object(Bucket=config.S3_BUCKET, Key=file_path)
        return s3_object['Body'].read().decode('utf-8')