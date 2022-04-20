import boto3
import json
import os

# Add an environment variable by entering "STATEMACHINEARN" under Key and pasting in our state machine's ARN under Value.
# STATEMACHINEARN ~ arn of state machine

stepfunctions_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    s3event = event['Records'][0]['s3']

    s3bucket = s3event['bucket']['name']
    s3key = s3event['object']['key']

    step_state = {
        "s3_bucket": s3bucket,
        "s3_audio_key": s3key
    }

    response = stepfunctions_client.start_execution(
        stateMachineArn=os.environ['STATEMACHINEARN'],
        input=json.dumps(step_state)
    )
    
    return json.dumps(response, default=str)
