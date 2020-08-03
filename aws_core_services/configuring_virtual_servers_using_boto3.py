# Import key libraries
import boto3

# Create an aws client
conn = boto3.client('ec2')

# Get aws response
# response = conn.create_security_group(GroupName='mywebgroup', Description='SG for Web')
# {'GroupId': 'sg-00a376a508b6e79c2', 'ResponseMetadata': {'RequestId': '1bce4dc8-fece-4e4d-a367-7d54aa244e90', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '1bce4dc8-fece-4e4d-a367-7d54aa244e90', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '283', 'date': 'Fri, 31 Jul 2020 09:44:20 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}

# Output response
# print(response)

# Configure server
# print(conn.authorize_security_group_ingress(GroupId='sg-00a376a508b6e79c2', IpProtocol='tcp', CidrIp='0.0.0.0/0',
#                                       FromPort=22, ToPort=22))

# Create a key pair
# keypair = conn.create_key_pair(KeyName='webkey')
# print(keypair)

# # Create an EC2 resources
ec2_conn = boto3.resource('ec2')
#
# # Create an instance
instance = ec2_conn.create_instances(MinCount=1, MaxCount=1, SecurityGroups=['mywebgroup'],
                                     KeyName = 'webkey', Instance='t2.micro')
print(instance)
