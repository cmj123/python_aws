# Import key libraries
import boto3
import json
import os
import threading
import sys

from boto3.s3.transfer import TransferConfig

# Define bucket name as a constant
BUCKET_NAME = 'aws-s3-2020-bucket'
WEBSITE_BUCKET_NAME = 'mys3esuawebsite.de'

# function - create a client
def s3_client():
    s3 = boto3.client('s3')
    return s3

# Function - Define s3 resources
def s3_resource():
    s3 = boto3.resource('s3')
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
                'Resource': 'arn:aws:s3:::' + bucket_name + '/*'
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

# Upload a small file to AWS
def upload_small_file():
    file_path = os.getcwd() + '/readme.txt'
    return s3_client().upload_file(file_path, BUCKET_NAME, 'readme.txt')

# Function - upload a large file
def upload_large_file():
    config = TransferConfig(multipart_threshold=1024 *25, max_concurrency=10,
                            multipart_chunksize= 1024*25, use_threads=True)
    file_path = os.getcwd() + '/Fate_Pitch_deck.pdf'
    key_path = 'multipart_files/largefile.pdf'
    s3_resource().meta.client.upload_file(file_path,BUCKET_NAME, key_path,
                                          ExtraArgs={'ACL':'public-read', 'ContentType':'text/pdf'},
                                          Config=config,
                                          Callback=ProgressPercentage(file_path))

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

        def __call__(self, bytes_amount):
            with self._lock:
                self._seen_so_far += bytes_amount
                percentage = (self._seen_so_far / self._size)*100
                sys.stdout.write(
                    "\r%s %s / %s (%.2f%%)"(
                        self._filename, self._seen_so_far, self._size, percentage
                    )
                )
                sys.stdout.flush()

# Function - reading objects and files
def read_object_from_bucket():
    object_key = 'readme.txt'
    return s3_client().get_object(Bucket=BUCKET_NAME, Key = object_key)

# Function - enable versioning
def version_bucket_files():
    s3_client().put_bucket_versioning(
        Bucket=BUCKET_NAME,
        VersioningConfiguration={
            'Status':'Enabled'
        }
    )

# Function - upload a new version
def upload_a_new_version():
    file_path = os.getcwd() + '/readme.txt'
    return s3_client().upload_file(file_path, BUCKET_NAME, 'readme.txt')

# Function - lifecycle policy configuration for buckets
def put_lifecycle_policy():
    lifecycle_policy = {
        "Rules":[
            {
                "ID": "Move readme file to Glacier",
                "Prefix": "readme",
                "Status":"Enabled",
                "Transitions":[
                    {
                        "Date":"2019-01-01T00:00:00.000Z",
                        "StorageClass": "GLACIER"
                    }
                ]
            },
            {
                "Status":"Enabled",
                "Prefix":"",
                "NoncurrentVersionTransitions":[
                    {
                        "NoncurrentDays":2,
                        "StorageClass": "GLACIER"
                    }
                ],
                "ID": "Move old versions to Glacier"
            }
        ]
    }

    s3_client().put_bucket_lifecycle_configuration(
        Bucket = BUCKET_NAME,
        LifecycleConfiguration = lifecycle_policy
    )

# Function - Host a website on AWS
def host_static_website():
    # Create client with the region close to me
    s3 = boto3.client('s3', region_name='eu-west-2')

    # Create  bucket
    s3.create_bucket(
        Bucket = WEBSITE_BUCKET_NAME,
        CreateBucketConfiguration = {
            'LocationConstraint' : 'eu-west-2'
        }
    )

    # Update policy
    update_bucket_policy(WEBSITE_BUCKET_NAME)

    # Website configuration
    website_configuration = {
        'ErrorDocument':{'Key':'error.html'},
        'IndexDocument':{'Suffix': 'index.html'}
    }

    s3_client().put_bucket_website(
        Bucket=WEBSITE_BUCKET_NAME,
        WebsiteConfiguration=website_configuration
    )

    index_file = os.getcwd() + '/index.html'
    error_file = os.getcwd() + '/error.html'

    s3_client().put_object(Bucket=WEBSITE_BUCKET_NAME, ACL='public-read', Key='index.html',
                           Body=open(index_file).read(), ContentType='text/html')
    s3_client().put_object(Bucket=WEBSITE_BUCKET_NAME, ACL='public-read', Key='error.html',
                           Body=open(error_file).read(), ContentType='text/html')

if __name__ == '__main__':
    ## Function - Create a bucket
    # print(create_bucket(BUCKET_NAME))
    # print('\n')
    ## Function - create a bucket policy
    # print(create_bucket_policy())
    ## Function - list aws buckets
    # print(list_buckets())
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
    ## Function - Upload a small file
    # print(upload_small_file())
    ## Function - Upload a large file
    # print(upload_large_file())
    # print(read_object_from_bucket())
    # print(version_bucket_files())
    # print(upload_a_new_version())
    # print(put_lifecycle_policy())
    print(host_static_website())
