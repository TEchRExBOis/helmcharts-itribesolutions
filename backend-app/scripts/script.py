import boto3
from botocore.exceptions import ClientError
import json

def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        # Attempt to retrieve the secret value
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle the exception based on error code
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise Exception("Secrets Manager can't decrypt the protected secret text using the provided KMS key.")
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise Exception("An error occurred on the server side.")
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise Exception("You provided an invalid value for a parameter.")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise Exception("You provided a parameter value that is not valid for the current state of the resource.")
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise Exception("We can't find the resource that you asked for.")
        else:
            raise e
    else:
        # Decrypts secret using the associated KMS key
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
            return binary_secret_data.decode('utf-8')

def save_secret_to_file(secret_data, file_path):
    # Format and save secret data to a file in environment variable format
    with open(file_path, 'w') as file:
        for key, value in secret_data.items():
            if isinstance(value, str) and " " in value:
                file.write(f'{key}="{value}"\n')  # Enclose the value in quotes if it contains spaces
            else:
                file.write(f'{key}={value}\n')

if __name__ == '__main__':
    # Define the secret name and AWS region
    SECRET_NAME = 'backend-env'
    REGION_NAME = 'us-east-2'

    # Fetch the secret
    secret = get_secret(SECRET_NAME, REGION_NAME)
    
    # Define the output file path
    OUTPUT_FILE = '/mnt/.env'
    
    # Save the fetched secret to the specified file
    save_secret_to_file(secret, OUTPUT_FILE)
    print(f"Secret saved to {OUTPUT_FILE}")