import boto3
import time
import logging

_logger = logging.getLogger(__name__)

def create_ec2_instance(region, image_id, instance_type, security_group, ec2_key_name, instance_name):
    try:
        ec2 = boto3.resource('ec2', region_name=region)
        instance = ec2.create_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            SecurityGroups=[
                security_group,
            ],
            MinCount=1,
            MaxCount=1,
            KeyName=ec2_key_name,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        }
                    ]
                }
            ]
        )
        instance_id = instance[0].id
        _logger.info(f"Created Instance: {instance_id}")
    except:
        _logger.exception(f"Instance Creation failed")
        raise
    wait_for_instance_ready(region, instance_id)
    return instance_id

def get_private_ip_from_id(region, instance_id):
    try:
        client = boto3.client('ec2', region_name=region)
        response = client.describe_instances(
            InstanceIds=[
                instance_id,
            ],
        )
        return response['Reservations'][0]['Instances'][0]['PrivateIpAddress']
    except:
        _logger.exception(f"Unable to fetch Private IP for Instance: {instance_id}")
        raise

def wait_for_instance_ready(region, instance_id, sleep_time=60, max_retries=10):
    try:
        retry = 1
        instance_status = 'pending'
        client = boto3.client('ec2', region_name=region)
        while instance_status not in('running', 'terminated', 'stopped') and retry < max_retries:
            _logger.info(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            response = client.describe_instance_status(
                InstanceIds=[
                    instance_id,
                ]
            )
            instance_status = response['InstanceStatuses'][0]['InstanceState']['Name']
            _logger.info(f"Current Instance State for Instance ID: {instance_id} in Region: {region}: {instance_status}")
            retry += 1
        if retry == max_retries:
            raise Exception(f"Max Retries exceeded while fetching state for Instance ID: {instance_id} in Region: {region}")
        elif instance_status in ('terminated', 'stopped'):
            raise Exception(f"Unknown error encountered while spawning Instance with Instance ID: {instance_id} in Region: {region}. Current state: {instance_status}")
        _logger.info(f"Instance: {instance_id} in Region: {region} is ready")
        return
    except:
        _logger.exception(f"Wait for Instance Ready failed for instance: {instance_id} in Region: {region}.")
        raise

def terminate_instance(region, instance_id):
    try:
        client = boto3.client('ec2', region_name=region)
        response = client.terminate_instances(
            InstanceIds=[
                instance_id,
            ]
        )
    except:
        _logger.exception(f"Error encountered while terminating Instance: {instance_id} in Region: {region}.")
        raise

def create_ami(region, instance_id, ami_name, terminate_node=False):
    try:
        client = boto3.client('ec2', region_name=region)
        response = client.create_image(
            InstanceId=instance_id,
            Name=ami_name
        )
        ami_id = response['ImageId']
        _logger.info(f"Create AMI: {ami_id}")
        wait_for_ami_ready(region, ami_id)
        if terminate_node:
            terminate_instance(region, instance_id)
        return ami_id
    except:
        _logger.exception(f"Unable to create AMI from Instance: {instance_id} in Region: {region}.")
        raise

def wait_for_ami_ready(region,ami_id, sleep_time=60, max_retries=10):
    try:
        retry = 1
        ami_status = "pending"
        client = boto3.client('ec2', region_name=region)
        while ami_status not in ('available', 'invalid', 'deregistered', 'failed', 'error') and retry < max_retries:
            _logger.info(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            response = client.describe_images(
                ImageIds=[
                    ami_id,
                ]
            )
            ami_status = response['Images'][0]['State']
            _logger.info(f"Current State for AMI ID: {ami_id} in Region: {region}: {ami_status}")
            retry += 1
        if retry == max_retries:
            raise Exception(f"Max Retries exceeded while fetching state for AMI ID: {ami_id} in Region: {region}")
        elif ami_status in ('invalid', 'deregistered', 'failed', 'error'):
            raise Exception(f"Unknown error encountered while creating image: {ami_id} in Region: {region}. Current state: {ami_status}")
        _logger.info(f"AMI: {ami_id} in Region: {region} is ready")
        return
    except:
        _logger.exception(f"Wait for AMI Ready failed for image: {ami_id} in Region: {region}.")
        raise

def get_ami_id_from_name(region, ami_name):
    try:
        client = boto3.client('ec2', region_name=region)
        response = client.describe_images(
            Filters=[
                {
                    'Name': 'name',
                    'Values': [
                        ami_name,
                    ]
                },
            ]
        )
        return response['Images'][0]['ImageId']
    except:
        _logger.exception(f"Unable to fetch AMI ID from Name: {ami_name} in Region:{region}.")
        raise