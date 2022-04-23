import json
import boto3
import cfnresponse
import threading
from elasticsearch import Elasticsearch
from time import sleep

def franken_load(endpoint, username, password):
    es = Elasticsearch(
        [{'host': endpoint, 'port': 443, 'use_ssl': True}],
        http_auth = (username, password)
    )

    es_ping = es.ping()
    print(f'Can connect to ES domain: {es_ping}')
    if es_ping == "False":
        print("Unable to connect to ES domain, waiting 10s and trying again")
        sleep(10)
        franken_load(endpoint, username, password)

    s3 = boto3.client('s3')
    frankenstein = json.loads(s3.get_object(
        Bucket = 'das-c01-data-analytics-specialty',
        Key = 'Labs/implementing-elasticsearch-microservice/frankenstein.json'
    )['Body'].read().decode())

    for i in frankenstein:
        try:
            es.index(index='frankenstein', doc_type='_doc', body=json.dumps(i), request_timeout = 60)
        except Exception as e:
            print(e)

def timeout(event, context):
    print('Timing out, sending failure response to CFN')
    cfnresponse.send(event, context, cfnresponse.FAILED, {}, None)

def handler(event, context):
    print(f'Received event: {json.dumps(event)}')
    timer = threading.Timer((context.get_remaining_time_in_millis() / 1000.00) - 0.5, timeout, args=[event, context])
    timer.start()

    status = cfnresponse.SUCCESS
    try:
        endpoint = event['ResourceProperties']['EsEndpoint']
        username = event['ResourceProperties']['ClusterUser']
        password = event['ResourceProperties']['ClusterPasword']

        franken_load(endpoint, username, password)

    except Exception as e:
        print(e)
        status = cfnresponse.FAILED
    finally:
        timer.cancel()
        cfnresponse.send(event, context, status, {}, None)