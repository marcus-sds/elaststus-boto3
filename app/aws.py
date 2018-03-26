__author__    = "Phil Hendren aka dizzythinks"
__credits__   = ["Phil Hendren"]
__version__   = "1.0"

from flask import current_app
import boto.ec2
import boto.ec2.autoscale
import boto.ec2.elb
import boto.ec2.cloudwatch
import boto.elasticache
import boto.rds
import boto.dynamodb
import boto.sqs
import boto.sns
import boto.cloudformation
import boto.route53
import boto.redshift
import boto3


def connect(account, region, service=None):
    aws_access_key_id = current_app.config['CONFIG']['accounts'][account]['aws_access_key_id']
    aws_secret_access_key  = current_app.config['CONFIG']['accounts'][account]['aws_secret_access_key']

    client=boto3.client('ec2',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name='us-east-1')
    regionsinfo=client.describe_regions()
    regions=regionsinfo['Regions']

    if service == 'ec2' or service == 'ebs' or service is None:
        bclient=boto3.client('ec2',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region)
        return bclient


    elif service == 'autoscale':
        bclient=boto3.client('autoscaling',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region)
        return bclient

    elif service == 'elb':
        conn = [x for x in boto.ec2.elb.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'rds':
        bclient=boto3.client('rds',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region)
        return bclient

    elif service == 'dynamodb':
        bclient=boto3.client(service,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region)
        return bclient

    elif service == 'elasticache':
        bclient=boto3.client(service,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region)
        return bclient

    elif service == 'sqs':
        conn = [x for x in boto.sqs.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'sns':
        conn = [x for x in boto.sns.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'cloudformation':
        conn = [x for x in boto.cloudformation.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'cloudwatch':
        conn = [x for x in boto.ec2.cloudwatch.regions() if x.name == region][0]
        conn = conn.connect(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
        return conn

    elif service == 'redshift':
        bclient=boto3.client(service,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name=region)
        return bclient


def r53():
    account = current_app.config['CONFIG']['route53']['account']
    aws_access_key_id = current_app.config['CONFIG']['accounts'][account]['aws_access_key_id']
    aws_secret_access_key  = current_app.config['CONFIG']['accounts'][account]['aws_secret_access_key']    
    domain = current_app.config['CONFIG']['route53']['domain']
    zone_id = current_app.config['CONFIG']['route53']['zone_id']
    c = boto.connect_route53(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    return c, domain, zone_id
