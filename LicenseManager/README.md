# Ubuntu LTS to Ubuntu Pro Upgrader

This script allows you to upgrade Ubuntu LTS instances to Ubuntu Pro at scale using AWS License Manager. It provides a main function and helper functions to perform the upgrade process.

## Prerequisites (your machine)

Before using this utility, make sure you have the following on your machine:

- Python 3.x installed on your system.
- AWS CLI configured with appropriate IAM credentials.
- Boto3 library installed. You can install it using the following command:

  ```
  pip install boto3
  ```

## Requirements (EC2 instances to be ugpraded)

  Ensure the following requirements are met on the EC2 machines you would like to upgrade:

  - The `ubuntu-advantage-tools` package should be up to date on each instance.
    ```
    sudo apt-get install -y ubuntu-advantage-tools
    ```
  - The instances should be managed by AWS Systems Manager (SSM).


## Usage

The main function in the script is `upgrade_instances_to_pro(instance_ids, version=None, wait=True)`. It takes the following parameters:

- `instance_ids` (list): A list of strings with instance IDs to convert.
- `version` (string, optional): If specified, it will be used to filter instances matching that version number. For example, `'18.04'` will upgrade all Ubuntu machines running 18.04 LTS. If not present, it will assume all versions.
- `wait` (bool, optional): By default, it will call the license conversion API and wait until it's done for each instance given. This can take longer to execute but will provide the conversion status in the process.

### Helper Functions

The script also provides some helper functions that can be used individually if needed:

- `get_instance_metadata(instance_id)`: Retrieve instance metadata for a single EC2 instance using its instance ID.
- `stop_instance_and_wait(instance_id)`: Stop a single EC2 instance using its instance ID. If the instance is already stopped, it returns `True`.
- `start_instance_and_wait(instance_id)`: Start an EC2 instance given its instance ID.
- `do_license_conversion(instance_id, waiting_time=5, wait_until_done=True)`: Calls the license conversion API for a given instance ID.

### Examples

Here are some examples of how to use the code:

1. Upgrade all the given Ubuntu LTS instances to Ubuntu Pro regardless of the version:

```
do_license_conversion(['i-1234abc','i-9786fedc','i-0001abc'])
```

2. Upgrade all your running Ubuntu 18.04 instances and wait for the result:

```
# Getting all instance IDs
ec2_client = boto3.client('ec2')
filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
response = ec2_client.describe_instances(Filters=filters)
instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]

# Calling the main upgrade function
upgrade_instances_to_pro(instance_ids, version='18.04')
```

3. Upgrade all your running Ubuntu 18.04 instances without waiting for the results:

```
# Getting all instance IDs
ec2_client = boto3.client('ec2')
filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
response = ec2_client.describe_instances(Filters=filters)
instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]

# Upgrading the 18.04 version without waiting
upgrade_instances_to_pro(instance_ids, version='18.04', wait=False)
```

## Notes

- The script assumes the script is run from an environment with appropriate AWS credentials and permissions.
- Ensure that you have the necessary access rights to perform the operations on EC2 instances, SSM, and License Manager.
- The script is written in Python 3.

## Limitations

- Check AWS License Manager limits before launching a massive upgrade, especially if running in parallel.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This utility is licensed under the [MIT License](LICENSE).

## Disclaimer

- Do not run this code before understanding its logic and testing it with a few instances first. Currently, downgrading from Ubuntu Pro cannot be done via self-service, and AWS support is required.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
