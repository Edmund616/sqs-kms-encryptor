import logging
from src.encryptor import list_sqs_queues, apply_kms_encryption

logging.basicConfig(level=logging.INFO)

def main():
    queues = list_sqs_queues()
    encrypted_count = 0

    for q in queues:
        if apply_kms_encryption(q):
            encrypted_count += 1

    logging.info(f"Done. Queues encrypted: {encrypted_count}")

if __name__ == '__main__':
    main()
