# https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
import boto3
import os

polly_client = boto3.client('polly')

def lambda_handler(event, context):
    payload = event['Input'][0]['Payload']
    payload_other = event['Input'][1]['Payload']

    payload.update(payload_other)

    translatedText = payload['TranslatedText']
    transcriptionJobName = payload['TranscriptionJobName']
    sentiment = payload['Sentiment']

    response = polly_client.start_speech_synthesis_task(
        LanguageCode=os.environ['LANGUAGECODE'],
        OutputFormat='mp3',
        OutputS3BucketName=os.environ['OUTPUTS3BUCKETNAME'],
        OutputS3KeyPrefix=f'{sentiment}/{transcriptionJobName}',
        Text=translatedText,
        TextType='text',
        VoiceId=os.environ['VOICEID']
    )

    return {
        'TaskId': response['SynthesisTask']['TaskId'],
        'TranscriptionJobName': transcriptionJobName
    }
