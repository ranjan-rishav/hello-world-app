from src import ec2
from src import cf
import argparse
import json
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
fh = logging.FileHandler("deploy.log",mode='a')
sh.setLevel(logging.INFO)
fh.setLevel(logging.DEBUG)
log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d]: %(message)s')
sh.setFormatter(log_format)
fh.setFormatter(log_format)
_logger.addHandler(sh)
_logger.addHandler(fh)

region = 'us-west-2'

resource_types = {
    "app_asg": "../inputs/helloworld/asg_with_dep.json",
    "app_alb": "../inputs/helloworld/app_alb.json",
    "natgw_rtb": "../inputs/common/natgw_rtb.json",
    "subnets": "../inputs/common/subnets.json"
}

def deploy_app(input_file_path):
    try:
        with open(input_file_path) as input_file:
            try:
                _logger.info(f"Reading CF Input JSON File: {input_file_path}")
                inputs_dict = json.load(input_file)
            except Exception as e:
                _logger.exception(f"Invalid Input JSON found at location: {input_file_path}.")
                raise
        try:
            _logger.info(f"Fetching required parameters from Input file.")
            resource_region = inputs_dict['aws']['region']
            stack_name = inputs_dict['stack']['name']
            template_path = inputs_dict['stack']['template_path']
            params = inputs_dict['stack']['parameters']
            _logger.debug(f"Following parameters will be used: {params}")
        except Exception as e:
            _logger.exception(f"Unable to fetch required parameters from Input file: {input_file_path}.")
            raise
        
        try:
            _logger.info(f"Initiating Stack Create/Update for Stack: {stack_name} in Region: {resource_region}")
            cf.create_update_stack(resource_region, stack_name, template_path, params)
        except Exception as e:
            _logger.exception(f"Stack Create/Update Failed for Stack: {stack_name} in Region: {resource_region}.")
            raise
    except Exception as e:
        _logger.exception(f"Unable to Create/Update Stack: {stack_name} in Region: {resource_region}. Error: {e}")
        raise


parser = argparse.ArgumentParser(description='Select appropriate operation')
parser.add_argument("-o", "--operation", dest="operation",
                    help="Name of Operation: get_ami_id_from_name|deploy", required=True)
parser.add_argument("-r", "--resource", dest="resource_type")
parser.add_argument("-a", "--ami-name", dest="ami")
args = parser.parse_args()


if args.operation == 'get_ami_id_from_name':
    if args.ami is None:
        raise Exception(f"Not all required arguments were passed.")
    ami_id = ec2.get_ami_id_from_name(region, args.ami)
    _logger.info(f"AMIID={ami_id}")
elif args.operation == 'deploy':
    if args.resource_type is None:
        raise Exception(f"Specify resource type with flag -r. Valid types: {list(resource_types.keys())}")
    elif args.resource_type not in resource_types.keys():
        raise Exception(f"Invalid Resource type Specified. Valid types: {list(resource_types.keys())}")
    else:
        deploy_app(resource_types[args.resource_type])
else:
    raise Exception(f"Incorrect Operation specified: {args.operation}")

