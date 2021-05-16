from src import ec2
import argparse
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
fh = logging.FileHandler("build.log",mode='a')
sh.setLevel(logging.INFO)
fh.setLevel(logging.DEBUG)
log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d]: %(message)s')
sh.setFormatter(log_format)
fh.setFormatter(log_format)
_logger.addHandler(sh)
_logger.addHandler(fh)

region = 'us-west-2'
# AMI with docker installed
base_ami_id = 'ami-0e15d1d4cad815f11' 

parser = argparse.ArgumentParser(description='Select appropriate operation')
parser.add_argument("-o", "--operation", dest="operation",
                    help="Name of Operation: create_ec2|create_ami", required=True)
parser.add_argument("-i", "--instance-id", dest="instance")
parser.add_argument("-a", "--ami-name", dest="ami")
args = parser.parse_args()

if args.operation == 'create_ec2':
    instance_id = ec2.create_ec2_instance(region, base_ami_id, 't2.micro', 'default', 'interim_instance', 'temp_instance')
    _logger.debug(f"Created Instance: {instance_id} in Region: {region} using base AMI: {base_ami_id}")
    _logger.info(f"PrivateIP={ec2.get_private_ip_from_id(region, instance_id)}")
    _logger.info(f"InstanceID={instance_id}")
elif args.operation == 'create_ami':
    if args.instance is None or args.ami is None:
        raise Exception(f"Not all required arguments were passed.")
    ami_id = ec2.create_ami(region, args.instance, args.ami, terminate_node=True)
    _logger.info(f"AMIID={ami_id}")
else:
    raise Exception(f"Invalid Operation: {args.operation} specified")
