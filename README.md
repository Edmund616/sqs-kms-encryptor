## Why SQS Encryption Is Necessary

Amazon SQS (Simple Queue Service) is a managed message queuing service that helps decouple microservices and distributed systems. However, the data passed through these queues can often be sensitive — containing user information, internal operations data, or system events.

Encrypting SQS messages at rest is essential for:
- **Data Security**: Prevent unauthorized access in case of data breach or compromised AWS account.
- **Compliance Requirements**: Encryption helps meet standards such as HIPAA, PCI-DSS, and GDPR.
- **Fine-Grained Access Control**: With KMS (Key Management Service), you can define which IAM roles/users can access or decrypt the messages.
- **Auditing and Logging**: AWS CloudTrail allows you to track the use of encryption keys, improving visibility into data access patterns.

In this project, we use a customer-managed KMS key to encrypt SQS messages, ensuring secure data transit between services.

Everything on this project has been thoroughly explained on my mediums post link below
https://medium.com/@divyln20/automatically-encrypt-your-aws-sqs-queues-with-kms-using-lambda-4bfe30c706ea
