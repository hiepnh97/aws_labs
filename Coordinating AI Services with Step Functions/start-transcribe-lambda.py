import boto3
import os
import uuid

transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    input = event['Input']
    s3Path = f"s3://{input['Bucket']}/{input['Key']}"
    jobName = f"{input['Key']}-{str(uuid.uuid4())}"

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode=os.environ['LANGUAGECODE'],
        Media={'MediaFileUri': s3Path},
        Settings={
            'ShowSpeakerLabels': False,
            'ChannelIdentification': False
        }
    )

    print(response)

    return {'TranscriptionJobName': response['TranscriptionJob']['TranscriptionJobName']}
