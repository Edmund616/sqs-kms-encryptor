import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')
kms_key_arn = os.environ.get('KMS_KEY_ARN')

def lambda_handler(event, context):
    logger.info("Starting SQS encryption process...")

    try:
        queues = sqs.list_queues().get('QueueUrls', [])
        if not queues:
            logger.info("No queues found.")
            return

        for queue_url in queues:
            # Get current attributes
            attrs = sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=["All"]
            )['Attributes']

            # Check if already encrypted
            if 'KmsMasterKeyId' in attrs and attrs['KmsMasterKeyId'] == kms_key_arn:
                logger.info(f"Queue already encrypted: {queue_url}")
                continue

            # Apply encryption
            sqs.set_queue_attributes(
                QueueUrl=queue_url,
                Attributes={
                    'KmsMasterKeyId': kms_key_arn,
                    'KmsDataKeyReusePeriodSeconds': '300'
                }
            )
            logger.info(f"Encrypted queue: {queue_url}")

    except Exception as e:
        logger.error(f"Error encrypting queues: {str(e)}")
        raise e
