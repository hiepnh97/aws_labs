import boto3
import json
import os
import urllib.request

translate_client = boto3.client('translate')

def lambda_handler(event, context):
    payload = event['Input']['Payload']
    transcriptFileUri = payload['TranscriptFileUri']
    transcriptionJobName = payload['TranscriptionJobName']

    transcriptFile = urllib.request.urlopen(transcriptFileUri).read()
    transcript = json.loads(transcriptFile)
    transcript_text = transcript['results']['transcripts'][0]['transcript']

    response = translate_client.translate_text(
        Text=transcript_text,
        SourceLanguageCode=os.environ['SOURCELANGUAGECODE'],
        TargetLanguageCode=os.environ['TARGETLANGUAGECODE']
    )

    return {
        'TranslatedText': response['TranslatedText'],
        'TranscriptionJobName': transcriptionJobName,
    }
