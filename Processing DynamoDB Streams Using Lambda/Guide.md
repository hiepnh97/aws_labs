# Processing DynamoDB Streams Using Lambda
## Reference
[DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)

## Introduction

In this lab, we will create a Lambda function to process DynamoDB stream data from an existing table that is actively being written to. Once processed, the data from the stream will be aggregated and written to a second DynamoDB table.

## Solution

Log in to the live AWS environment using the credentials provided. Make sure you're in the N. Virginia (`us-east-1`) region throughout the lab.

### Create a Lambda Function to Process Stream Events

1. Navigate to **Lambda** > **Functions**.

2. Click **Create function**.

3. Make sure the **Author from scratch** option at the top is selected, and then use the following settings:

    - *Function name*: **TaTourneyStats**
    - *Runtime*: **Python 3.7**

4. Expand **Choose or create an execution role**, and use the following settings:

    - *Execution role*: **Use an existing role**
    - *Existing role*: Select the only role listed

5. Click **Create function**.

6. Scroll down to **Function Code**.

7. Delete the existing code and replace it with the following script:

```
import json
import boto3

print('Loading function...')
def writestats(newrecord):
    ddbClient = boto3.client('dynamodb')

    try:
        currentStats = ddbClient.get_item(
            TableName = 'TaTourneyStats',
            Key = {
                'player': newrecord['player']
            }
        )
    except Exception as e:
        print(e)
        return e

    if 'Item' not in currentStats.keys():
        statItem = {
            'player': newrecord['player'],
            'avg_score': newrecord['score'],
            'games': {'N': '1'}
        }
        if 'winner' in newrecord.keys():
            statItem['wins'] = {'N': '1'}
        else:
            statItem['wins'] = {'N': '0'}

        statItem['win_percent'] = {'S': f"{str((int(statItem['wins']['N']) / int(statItem['games']['N']))*100)[:5]}%"}
        print(f'New Record: {statItem}')
        try:
            ddbClient.put_item(
                TableName = 'TaTourneyStats',
                Item = statItem
            )
        except Exception as e:
            print(e)
            return e

    else:
        statItem = {
            'games': {'N': str(int(currentStats['Item']['games']['N']) + 1)}
        }

        if 'winner' in newrecord.keys():
            statItem['wins'] = {'N': '1'}
        else:
            statItem['wins'] = {'N': '0'}

        statItem['win_percent'] = {'S': f"{str(((int(currentStats['Item']['wins']['N']) + int(statItem['wins']['N'])) / int(statItem['games']['N']))*100)[:5]}%"}

        statItem['avg_score'] = {'N': str((int(currentStats['Item']['avg_score']['N']) + int(newrecord['score']['N'])) // 2)}
        print(f'Update: {statItem}')
        try:
            ddbClient.update_item(
            ExpressionAttributeValues={
                ':avs': statItem['avg_score'],
                ':win': statItem['wins'],
                ':wp': statItem['win_percent'],
                ':one': {'N': '1'}
            },
            UpdateExpression='SET avg_score = :avs, games = games + :one, wins = wins + :win, win_percent = :wp',
            Key={
                'player': newrecord['player']
            },
            TableName = 'TaTourneyStats'
        )
        except Exception as e:
            print(e)
            return e

def lambda_handler(event, context):
    for record in event['Records']:
        if 'NewImage' in record['dynamodb'].keys():
            print(json.dumps(record['dynamodb']['NewImage']))
            print(writestats(record['dynamodb']['NewImage']))

    successmsg = f'Successfully processed {len(event["Records"])} records.'
    print(successmsg)
    return successmsg
```

8. Click **Save**.

### Create a DynamoDB Streams Trigger

1. In the **Designer** section, click **Add trigger**.

2. On the Add trigger page, set the following values:

    - **Trigger configuration**: DynamoDB
    - **DynamoDB table**: TaTourney
    - **Batch size**: 10
    - **Batch window**: 0
    - **Starting position**: Trim horizon

3. Leave the rest as their default and click Add

    .

    > **Note:** It may take several minutes for the trigger to be added.

4. Navigate back to the **TaTourneyStats** page.

5. Scroll down to **Basic settings** section.

6. In **Timeout**, set the maximum to **30** seconds.

7. Click **Save**.

### Verify Stream Processing

1. Navigate to DynamoDB.
2. On the left menu, select **Tables**.
3. Select **TaTourneyStats**.
4. Select the **Items** tab.
5. Verify that the statistics are correctly aggregated and written to the TaTourneyStats table.