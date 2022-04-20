import boto3

transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    payload = event['Input']['Payload']
    transcriptionJobName = payload['TranscriptionJobName']

    response = transcribe_client.get_transcription_job(
        TranscriptionJobName=transcriptionJobName
    )

    transcriptionJob = response['TranscriptionJob']

    transcriptFileUri = "none"
    if 'Transcript' in transcriptionJob:
        if 'TranscriptFileUri' in transcriptionJob['Transcript']:
            transcriptFileUri = transcriptionJob['Transcript']['TranscriptFileUri']

    return {
        'TranscriptFileUri': transcriptFileUri,
        'TranscriptionJobName': transcriptionJobName,
        'TranscriptionJobStatus': transcriptionJob['TranscriptionJobStatus']
    }
