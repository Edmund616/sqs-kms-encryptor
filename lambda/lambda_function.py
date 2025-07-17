from src.encryptor import list_sqs_queues, apply_kms_encryption
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    queues = list_sqs_queues()
    encrypted_count = 0

    for q in queues:
        if apply_kms_encryption(q):
            encrypted_count += 1

    logger.info(f"Lambda finished. Queues encrypted: {encrypted_count}")
    return {
        "statusCode": 200,
        "body": f"Encrypted {encrypted_count} queues"
    }
