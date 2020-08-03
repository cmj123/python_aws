# Import key libraries
import boto3
import json

# Define bucket name as a constant
BUCKET_NAME = 'aws-s3-2020-bucket'
# function - create a client
def s3_client():
    s3 = boto3.client('s3')
    return s3

# Create an s3 bucket
def create_bucket(bucket_name):
    return s3_client().create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint':'eu-west-2'
        }
    )

# Create a bucket policy
def create_bucket_policy():
    bucket_policy = {
        "Version":"2012-10-17",
        "Statement": [
            {
                "Sid":"AddPerm",
                "Effect":"Allow",
                "Principal":"*",
                "Action":["s3:*"],
                "Resource":["arn:aws:s3:::aws-s3-2020-bucket/*"]
            }
        ]
    }

    # Dump policy
    policy_string = json.dumps(bucket_policy)

    return s3_client().put_bucket_policy(
        Bucket = BUCKET_NAME,
        Policy = policy_string
    )

# Function - list aws buckets
def list_buckets():
    return s3_client().list_buckets()

# Function - Get a bucket's policy
def get_bucket_policy():
    return s3_client().get_bucket_policy(Bucket=BUCKET_NAME)

# Function - get a bucket's encryption
def get_bucket_encryption():
    return s3_client().get_bucket_encryption(Bucket=BUCKET_NAME)

# Function - update a bucket's policy
def update_bucket_policy(bucket_name):
    bucket_policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'AddPerm',
                'Effect':'Allow',
                'Principal': '*',
                'Action':[
                    's3:DeleteObject',
                    's3:GetObject',
                    's3:PutObject'
                ],
                'Resource': ["arn:aws:s3:::aws-s3-2020-bucket/*"]
            }
        ]

    }

    policy_string = json.dumps(bucket_policy)

    return s3_client().put_bucket_policy(
        Bucket=bucket_name,
        Policy=policy_string
    )
# Function to enable encryption
def server_side_encrypt_bucket():
    return s3_client().put_bucket_encryption(
        Bucket = BUCKET_NAME,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm':'AES256'
                    }
                }
            ]
        }
    )

# Function - Delete a bucket
def delete_bucket():
    return s3_client().delete_bucket(Bucket=BUCKET_NAME)

if __name__ == '__main__':
    ## Function - Create a bucket
    # print(create_bucket(BUCKET_NAME))
    ## Function - create a bucket policy
    # print(create_bucket_policy())
    ## Function - list aws buckets
    print(list_buckets())
    ## Function - Get bucket policy
    # print(get_bucket_policy())
    ## Function - get a bucket's encryption
    # print(get_bucket_encryption())
    ## # Function - update a bucket's policy
    # print(update_bucket_policy(BUCKET_NAME))
    # Function to enable encryption
    # print(server_side_encrypt_bucket())
    ## Function to delete a bucket
    # print(delete_bucket())
