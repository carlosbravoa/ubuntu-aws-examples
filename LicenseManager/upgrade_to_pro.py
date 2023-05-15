#!/usr/bin/python3
# coding: utf-8
'''
Script for upgrading Ubuntu LTS instances to Ubuntu Pro at scale.
Requirements: 
    - `ubuntu-advantage-tools` package up to date on each instance
    - Having instances managed by SSM
    
The main function is: 
    upgrade_instances_to_pro(instance_ids, version=None, wait=True):

    Params: 
    instance_ids (list): A list of strings with instance IDs to convert
    version (string): If is specified, it will be used to filter instances matching 
                    that version number, e.g. '18.04' to upgrade all Ubuntu machines
                    running 18.04 LTS. If not present will assume all versions.
    wait (bool): By default will call the license conversion API and wait until done
                 for each instance given. This can take longer to execute but will
                 provide the conversion status in the process.

helper functions:
- get_instance_metadata(instance_id)
- stop_instance_and_wait(instance_id)
- start_instance_and_wait(instance_id)
- do_license_conversion(instance_id, waiting_time=5, wait_until_done=True)

Examples:

1. Calling upgrade to all the given instances regardless of the version
    `do_license_conversion(['i-1234abc','i-9786fedc','i-0001abc'])`
    
2. Calling upgrade to all my 18.04 instances, waiting for the result:

```
# getting all my instance ids:
ec2_client = boto3.client('ec2')
filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
response = ec2_client.describe_instances(Filters=filters)
instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]

# Calling the main upgrade function:
upgrade_instances_to_pro(instance_ids, version='18.04')
```

3. Calling the upgrade for all my instances without waiting for the results:
```
# getting all my instance ids:
ec2_client = boto3.client('ec2')
filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
response = ec2_client.describe_instances(Filters=filters)
instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]

# upgrading the 18.04 version, without waiting 
upgrade_instances_to_pro(instance_ids, version='18.04', wait=False)
```

'''

import boto3
import time

REGION='us-east-1'
ACCOUNT=''

def get_instance_metadata(instance_id):
    """
    Retrieve instance metadata for a single EC2 instance using its instance ID.

    Args:
        instance_id (str): The ID of the EC2 instance to retrieve metadata for.

    Returns:
        dict: A dictionary containing the relevant metadata for the specified instance, including:
            - InstanceId: The ID of the instance.
            - PlatformDetails: The details of the platform running on the instance.
            - UsageOperation: The usage operation of the instance (e.g. On-Demand).
            - PlatformName: The name of the platform running on the instance.
            - PlatformVersion: The version of the platform running on the instance.

        Returns None if an error occurs.
    """
    # Create an EC2 and SSM clients
    ec2 = boto3.client('ec2')
    ssm = boto3.client('ssm')
    
    
    # Retrieve the instance metadata
    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance_data = response['Reservations'][0]['Instances'][0]
        platform_details = instance_data.get('PlatformDetails', 'N/A')
        usage_operation = instance_data.get('UsageOperation', 'N/A')

        # Retrieve the PlatformName and PlatformVersion metadata from SSM
        response = ssm.describe_instance_information(
            InstanceInformationFilterList=[
                {
                    'key': 'InstanceIds',
                    'valueSet': [instance_id]
                }
            ]
        )
       
        platform_name = response['InstanceInformationList'][0]['PlatformName']
        platform_version = response['InstanceInformationList'][0]['PlatformVersion']

        # Add the instance metadata and SSM metadata to the instance dictionary
        instance_metadata = {
            'InstanceId': instance_id,
            'PlatformDetails': platform_details,
            'UsageOperation': usage_operation,
            'PlatformName': platform_name,
            'PlatformVersion': platform_version
        }

        return instance_metadata

    except Exception as e:
        print(f"Error retrieving metadata for instance {instance_id}: Is the instance online and managed by SSM?")

    
def stop_instance_and_wait(instance_id):
    """
    Stop a single EC2 instance using its instance ID.
    If instance is already stopped, returns True

    Args:
        instance_id (str): The ID of the EC2 instance to stop.

    Returns:
        bool: True if the instance was successfully stopped, False otherwise.
    """
    ec2 = boto3.client('ec2')

    try:
        print(f"Stopping instance {instance_id}")
        # Stop the instance
        ec2.stop_instances(InstanceIds=[instance_id])
        
        # Wait until the instance is stopped
        waiter = ec2.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[instance_id])
        
        # Return True if the instance was successfully stopped
        print(f"Instance {instance_id} stopped")
        return True

    except ec2.exceptions.ClientError as e:
        print(f"Error stopping instance {instance_id}: {e}")
        return False

def start_instance_and_wait(instance_id):
    """
    Start an EC2 instance given its instance ID.

    Args:
        instance_id (str): The ID of the EC2 instance to start.

    Returns:
        bool: True if the instance was successfully started, False otherwise.
    """
    try:
        ec2_client = boto3.client('ec2')
        
        print(f"Starting instance {instance_id}")
        response = ec2_client.start_instances(InstanceIds=[instance_id])
        instance_state = response['StartingInstances'][0]['CurrentState']['Name']
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])

        print(f"Instance {instance_id} started")
        return True

    except Exception as e:
        print(f"Error starting instance {instance_id}: {e}")
        return False


def do_license_conversion(instance_id, waiting_time=5, wait_until_done=True):
    """
    Calls the license conversion API for a given instance ID

    Args:
        instance_id (str): The ID of the EC2 instance to start.
        waiting_time (int): Seconds for polling the conversion status. 
                            Default is 5 seconds
    Returns:
        bool: True if the instance was successfully converted, False otherwise.
    """
    
    instance_arn = f"arn:aws:ec2:{REGION}:{ACCOUNT}:instance/{instance_id}"
    result = None
    
    try:
        print(f"Starting license conversion for instance {instance_id} ")
        client = boto3.client('license-manager')
        response = client.create_license_conversion_task_for_resource(
            ResourceArn=instance_arn,
            SourceLicenseContext={
                'UsageOperation': 'RunInstances'
            },
            DestinationLicenseContext={
                'UsageOperation': 'RunInstances:0g00'
            }
        )

        task_id = response['LicenseConversionTaskId']
        print(f"License conversion started with id: {task_id}", end=" ")
        
        # Check if the task was successful
        if wait_until_done:
            while not result:

                task = client.get_license_conversion_task(LicenseConversionTaskId=task_id)

                if task['Status'] == 'SUCCEEDED':
                    print(f"\nInstance {instance_id} successfully converted")
                    result = True
                elif task['Status'] == 'FAILED':
                    print(f"\nConversion of {instance_id} failed. You can check logs on SSM Run Command console")
                    result = False
                else:
                    print(".", end="") # to show something is still going on
                    time.sleep(waiting_time) #wait and retry
            return result
            
    except Exception as e:
        print(f"Error performing license conversion for instance {instance_id}: {e}")
        
        return False


def upgrade_instances_to_pro(instance_ids, version=None, wait=True):
    '''
    Main function for upgrading Ubuntu LTS to Ubuntu Pro using AWS License 
    Manager. It goes one by one, but it can be parallelized by adding to 
    `do_license_conversion` an extra param: wait_until_done=False
    
    Args:
        instance_ids (list): A list with instance ids
        version (string): The Ubuntu version number e.g. 16.04, 18.04, etc
                        if None or not present then it will upgrade all Ubuntu 
                        instances regardless of the version
    '''
    ec2 = boto3.client('ec2')
    
    for instance in instance_ids:
        
        print(f"\n**** Trying instance {instance} ****")
        
        # 1. Check whether the instance is upgradable
        try:
            instance_data = get_instance_metadata(instance)
            if not instance_data:
                continue

            # 2. Check platform, platform version and current license
            isUbuntu = instance_data.get('PlatformName') == 'Ubuntu'
            isVersion = instance_data.get('PlatformVersion') == version if version else True
            isEligible = instance_data.get('UsageOperation') == 'RunInstances'

            if isUbuntu and isVersion and isEligible:

                # 3. Stop the instance
                stopped = stop_instance_and_wait(instance)
                if not stopped:
                    continue # The error is printed already, skip to next instance

                # 4. Call the license conversion
                converted = do_license_conversion(instance, wait_until_done=wait)
                if not converted:
                    continue

                # 5. Start the instance
                started = start_instance_and_wait(instance)
                if not started:
                    continue
            else:
                print(f"* Instance {instance} doesn't meet the criteria specified:")
                print(instance_data)
        except Exception as e:
            print(f"Error getting information for {instance}: {e}")
    print("Done")
        




