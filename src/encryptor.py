import boto3
import logging
from botocore.exceptions import ClientError

sqs = boto3.client('sqs')
kms_key_id = 'alias/aws/sqs'  # Replace with your KMS key alias or full ARN

def list_sqs_queues():
    try:
        response = sqs.list_queues()
        return response.get('QueueUrls', [])
    except ClientError as e:
        logging.error(f"ListQueues error: {e}")
        return []

def apply_kms_encryption(queue_url):
    try:
        attributes = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['All']
        )['Attributes']

        if 'KmsMasterKeyId' in attributes:
            logging.info(f"Already encrypted: {queue_url}")
            return False

        sqs.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={
                'KmsMasterKeyId': kms_key_id,
                'KmsDataKeyReusePeriodSeconds': '300'
            }
        )
        logging.info(f"Encrypted: {queue_url}")
        return True

    except ClientError as e:
        logging.error(f"Encryption error for {queue_url}: {e}")
        return False
