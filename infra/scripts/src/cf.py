import boto3
import time
from botocore.exceptions import ClientError
import logging

_logger = logging.getLogger(__name__)

success_statuses = ["CREATE_COMPLETE", "DELETE_COMPLETE", "UPDATE_COMPLETE"]
failure_statuses = ["CREATE_FAILED", "DELETE_FAILED", "ROLLBACK_FAILED", "UPDATE_ROLLBACK_FAILED"]
rollback_success_statuses = ["ROLLBACK_COMPLETE", "UPDATE_ROLLBACK_COMPLETE"]
in_progress_statuses = ["IN_PROGRESS", "CREATE_IN_PROGRESS", "DELETE_IN_PROGRESS", "ROLLBACK_IN_PROGRESS", "UPDATE_IN_PROGRESS", "UPDATE_ROLLBACK_IN_PROGRESS", "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS", "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS"]

def create_update_stack(region, stack_name, template_path, parameters):
    try:
        client = boto3.client('cloudformation', region)
        try:
            _logger.info(f"Fetching template file: {template_path}")
            with open(template_path, 'r') as template_file:
                template_file_contents = template_file.read()
                _logger.debug(f"Contents of template file:\n{template_file_contents}")
        except:
            _logger.exception(f"Unable to read template file: {template_path}.")
            raise
        try:
            response = client.validate_template(
                TemplateBody=template_file_contents
            )
            _logger.info(f"Template Validation passed...")
        except:
            _logger.exception(f"Template Validation failed for Stack: {stack_name} and Body: {template_path}.")
            raise
        if get_stack_status(region, stack_name):
            response = client.update_stack(
                StackName=stack_name,
                TemplateBody=template_file_contents,
                Parameters=parameters
            )
            _logger.info(f"Update Stack Operation triggered for Stack: {stack_name}")
        else:
            response = client.create_stack(
                StackName=stack_name,
                TemplateBody=template_file_contents,
                Parameters=parameters
            )
            _logger.info(f"Create Stack Operation triggered for Stack: {stack_name}")
        wait_for_stack_ready(region, stack_name)
        _logger.info(f"Operation Complete for Stack: {stack_name} in Region: {region}")
    except:
        _logger.exception(f"Stack Creation failed for Stack: {stack_name} in Region: {region}")
        raise

def get_stack_status(region, stack_name):
    try:
        client = boto3.client('cloudformation', region)
        response = client.describe_stacks(
            StackName=stack_name
        )
        return response['Stacks'][0]['StackStatus']
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ValidationError':
            _logger.exception(f"Stack: {stack_name} in Region: {region} does not exist.")
            return False
        else:
            _logger.exception(f"Error while fetching status for Stack: {stack_name} in Region: {region}.")
            raise
    except:
        _logger.exception(f"Error while fetching status for Stack: {stack_name} in Region: {region}")
        raise

def wait_for_stack_ready(region, stack_name, sleep_time=60, max_retries=20):
    try:
        stack_status = "IN_PROGRESS"
        retry = 1
        _logger.info(f"Waiting for Stack: {stack_name} in Region: {region} to be ready")
        while stack_status in in_progress_statuses and retry < max_retries:
            _logger.info(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
            stack_status = get_stack_status(region, stack_name)
            retry += 1
        if retry == max_retries:
            raise Exception(f"Max retries: {max_retries} exceeded. Last Status for Stack: {stack_name} in Region: {region} is: {stack_status}")
        elif stack_status in success_statuses:
            _logger.info(f"Current Status for Stack: {stack_name} in Region: {region} is: {stack_status}")
            return
        elif stack_status in failure_statuses:
            raise Exception(f"Current Status for Stack: {stack_name} in Region: {region} is: {stack_status}")
        elif stack_status in rollback_success_statuses:
            _logger.info(f"Current Status for Stack: {stack_name} in Region: {region} is: {stack_status}")
        elif not stack_status:
            _logger.info(f"Stack: {stack_name} in Region: {region} does not exist")
        else:
            raise Exception(f"No matches found for received Status: {stack_status} for Stack: {stack_name} in Region: {region}")
    except:
        _logger.exception(f"Error while waiting for Stack: {stack_name} in Region: {region}.")
        raise
