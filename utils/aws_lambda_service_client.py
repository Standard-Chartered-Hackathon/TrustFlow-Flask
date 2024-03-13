import json
from config import aws_access_key_id, aws_secret_access_key, aws_region
import boto3


def invoke_lambda(function_name, data=None, invocation_type=None):
    client = boto3.client(
                        'lambda',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=aws_region
                        )
    if data is None:
        payload = data
    else:
        payload = json.dumps(data).encode("utf-8")
    if invocation_type == "Event":
        lambda_params = {
            "FunctionName": function_name,
            "InvocationType": invocation_type,
            "Payload": payload,
        }
        client.invoke(**lambda_params)
    else:
        lambda_params = {
            "FunctionName": function_name,
            "InvocationType": 'RequestResponse',
            "Payload": payload,
        }
        response = client.invoke(**lambda_params)
        response = json.loads(response["Payload"].read().decode("utf-8"))
        return response
