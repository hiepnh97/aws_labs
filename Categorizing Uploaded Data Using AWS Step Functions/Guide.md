# Categorizing Uploaded Data Using AWS Step Functions

## Introduction

AWS provides Step Functions as a way to help manage the flow of information through a pipeline of steps. This includes calling services such as Lambda, Glue, Athena, and DynamoDB, as well as performing some basic decisions and waiting for things to complete. Step Functions allow you to move state information in between steps and act on the state. In this lab, we'll build a serverless pipeline to translate audio to text, and sort the data based on keywords in the transcript.

## Solution

Use a new Incognito or Private browser window to log in to the lab. This ensures that your personal account credentials, which may be active in your main window, are not used for the lab.

Log in to the AWS console using the account credentials provided with the lab. Please make sure you are in the `us-east-1` (N. Virginia) region when in the AWS console.

### Prepare to Launch the Step Function

#### Create an IAM Role

1. In the search bar, search for "IAM".
2. Select **IAM** from the search results.
3. In the lefthand menu, click on **Roles**.
4. Click the **Create role** button.
5. Click **Step Functions** from the list use of use cases.
6. Click **Next: Permissions**.
7. Since the *AWSLambdaRole* permissions policy is already attached, click **Next: Tags**.
8. Create a tag by entering "app" under *Key* and "meeting-transcriber" under *Value*.
9. Click **Next: Review**.
10. In *Role name*, enter the name "step-functions-lambda-role".
11. Click **Create role**. This will create an IAM role to allow Step Functions to start Lambda functions.

#### Create a Step Function

1. In the search bar at the top of the console, search for "Step Functions."
2. Select **Step Functions** from the results.
3. Click the **Get started** button.
4. Click the hamburger menu icon (the icon with the three horizontal lines) in the top left corner.
5. Click **State machines**.
6. Click the **Create state machine** button.
7. Select **Author with code snippets**.
8. Under *Type*, select **Standard**.
9. Click **Next**.
10. Under *Name*, enter the name "Categorize-Audio-Data-Pipeline" in the *State machine name* field.
11. Click **Choose an existing role** and make sure the role is the one that we just created.
12. Under *Tags - optional*, create a tag by entering "app" under *Key* and "meeting-transcriber" under *Value*.
13. Click **Create state machine**.
14. Under *ARN* in *Details*, copy the ARN into your clipboard.

#### Update Lambda and S3 to Work with Step Functions

1. In the search bar, type "lambda".
2. Select **Lambda** from the search results and open it in a new browser window or tab.
3. Under *Function name*, click **run-step-functions-lambda**.
4. Under *Function code*, click **index.py**.
5. In the Python file, note that it contains a placeholder at the end called `STATEMACHINEARN`.
6. Under the *Configuration* tab in the *Environmental variables* section, click **Edit**.
7. Click **Add environment variable**.
8. Add an environment variable by entering "STATEMACHINEARN" under *Key* and pasting in our state machine's ARN under *Value*.
9. Click the **Save** button.
10. In the search bar on top, type "s3".
11. Select **S3** from the search results and open it in a new tab.
12. Make sure that the access for the provided bucket is set to *Bucket and objects not public*.
13. Click on the provided bucket.
14. Click the **Properties** tab.
15. Under *Event notifications*, click **Create event notification**.
16. Under *General configuration*, set the following values:

- In *Event name*, enter the name "trigger-audio-processing-event".
- In *Prefix - optional*, enter "upload/".
- In *Suffix - optional*, enter ".mp3".

1. Select the checkbox next to **All object create events**.
2. In the dropdown menu under *Lambda function*, select the **run-step-functions-lambda** function that we just created.
3. Click **Save changes**.

### Create the Step Function Pipeline

#### Create a Transcribe Job

1. Return to the browser window or tab with the Step Functions console open.

2. Click **Edit**.

3. From the code snippet, delete the `Hello` and `World` states after `"States": {`.

4. In the *Generate code snippet* dropdown, select **AWS Lambda: Invoke a function**.

5. In the *Select function from a list* dropdown menu, select our **transcribe-audio-lambda** function.

6. Click **Copy to clipboard**.

7. Paste the code into the code snippet after `"States": {`.

8. Click **Format JSON**.

9. Rename `Invoke lambda function` to:

    `Start Transcription `

10. At `"Startat": Hello`, replace `Hello` with:

    `Start Transcription `

#### Create a Wait State

1. In the *Generate code snippet* dropdown, select **Wait state**.

2. Click **Copy to clipboard**.

3. Paste it under the `},` that is under `"Next": "NEXT_STATE"`.

4. Click **Format JSON**.

5. Replace `Wait State` with:

    `Wait for Transcribe `

6. Change `"Seconds": 5,` to:

    `"Seconds": 30, `

7. In the `Start Transcription` state, change `"NEXT_STATE"` to:

    `"Wait for Transcribe" `

8. In the *Generate code snippet* dropdown, select **AWS Lambda: Invoke a function**.

9. In the *Select function from a list* dropdown menu, select our **transcribe-status-lambda** function.

10. Click **Copy to clipboard**.

11. Paste it under the `},` that is under `"Next": "NEXT_STATE"`.

12. Click **Format JSON**.

13. Rename `Invoke lambda function` to:

    `Check Transcribe Status `

14. In the `Wait State` state, change `"NEXT_STATE"` to:

    `"Check Transcribe Status" `

#### Create a Completed and Failed State

1. In the *Generate code snippet* dropdown, select **Choice state**.

2. Click **Copy to clipboard**.

3. Paste it under the `},` that is under `"Next": "NEXT_STATE"`.

4. Replace `Choice State` with:

    `Is Transcribe Complete `

5. In the `Check Transcribe Status` state, change `"NEXT_STATE"` to:

    `"Is Transcribe Complete" `

6. Click **Format JSON**.

7. Under `"Choices": [`, delete the `"Not": {` block.

8. Delete the `"And": {` block.

9. Copy the block under `"Choices": [` and paste it under the existing block.

10. In the first Choices block, replace `NumericEquals` to `StringEquals` and replace `0` with `COMPLETED`.

11. In the second Choices block, replace `NumericEquals` to `StringEquals` and replace `0` with `FAILED`.

12. In the first Choices block, replace `$.value` with:

    `$.Payload.TranscriptionJobStatus `

13. In the second Choices block, replace `$.value` with:

    `$.Payload.TranscriptionJobStatus `

14. Replace `DEFAULT_STATE` with:

    `Wait for Transcribe `

15. In the *Generate code snippet* dropdown, select **AWS Lambda: Invoke a function**.

16. In the *Select function from a list* dropdown menu, select our **categorize-data-lambda** function.

17. Click **Copy to clipboard**.

18. Paste it under the `},` that is under `"Default": "Wait For Transcribe"`.

19. Click **Format JSON**.

20. Rename `Invoke Lambda function` to:

    `Categorize Data `

21. In the Completed block for Choices, replace `NEXT_STATE_TWO` with `Categorize Data`.

22. In the `Categorize Data` block, replace `"Next": "NEXT_STATE"` with:

    `"End": true `

23. In the *Generate code snippet* dropdown, select **Fail state**.

24. Click **Copy to clipboard**.

25. 1. Paste it under the `},` that is under `"End": true`.

26. Click **Format JSON**.

27. Replace `Fail State` with:

    `Transcribe Failed `

28. Delete the `"Error"` and `"Cause"` lines.

29. In the Failed block for Choices, replace `NEXT_STATE_TWO` with:

    `Transcribe Failed `

30. Click **Save**.

31. Click **Save anyway**.

### Create the Lambda Business Logic

#### Write the Transcribe Audio Function

1. Return to the browser window or tab with the Lambda functions console open.

2. Click on **transcribe-audio-lambda**.

3. Under *Function code*, click on **index.py**.

4. In the `s3 bucket` line, replace the placeholder at the end with:

    `step_state['s3_bucket'] `

5. In the `s3 audio_key` line, replace the placeholder at the end with:

    `step_state['s3_audio_key'] `

6. In the `meeting_audio_URI` line, replace the placeholder at the end with:

    `f's3://{s3_bucket}/{s3_audio_key}' `

7. In the `jobName` line, replace the placeholder at the end with:

    `f'{s3_audio_key}-{str(uuid.uuid4())}'.replace('/','-') `

8. In the `transcript_key` line, replace the placeholder at the end with:

    `f'transcripts/{s3_audio_key}-transcript.json' `

9. In the `step_state['transcript_key']` line, replace the placeholder at the end with:

    `transcript_key `

10. In the `step_state['TranscriptionJobName` line, replace the placeholder at the end with:

    `response['TranscriptionJob']['TranscriptionJobName'] `

11. Click **Deploy**.

#### Write the Transcribe Status Function

1. Return to the browser tab or window with the Lambda functions console.

2. Click on **transcribe-status-lambda**.

3. Under *Function code*, click on **index.py**.

4. In the `transcriptionJobName` line, replace the placeholder at the end with:

    `step_state['TranscriptionJobName'] `

5. In the `step_state['TranscriptionJobStatus']` line, replace the placeholder at the end with:

    `response['TranscriptionJob']['TranscriptionJobStatus'] `

6. Click **Deploy**.

#### Write the Categorize Data Function

1. Return to the browser window or tab with the Lambda functions console.

2. Click on **categorize-data-lambda**.

3. Under *Function code*, click on **index.py**.

4. In the `step_state` line, replace the placeholder at the end with:

    `event['Input']['Payload'] `

5. In the `s3_bucket` line, replace the placeholder at the end with:

    `step_state['s3_bucket'] `

6. In the `s3_audio_key` line, replace the placeholder at the end with:

    `step_state['s3_audio_key'] `

7. In the `s3_transcript_key` line, replace the placeholder at the end with:

    `step_state['transcript_key'] `

8. Under *Environment Variables*, click **Edit**.

9. Click **Add environmental variable**.

10. Under *Key*, enter "KEYWORDS", and under *Value*, enter "important".

11. Click **Save**.

12. In the `output_date` line, replace the placeholder at the end with:

    `date.today().strftime('%Y/%m/%d') `

13. In the `output_folder` line, replace the placeholder at the end with:

    `'important' if contains_keyword else 'processed' `

14. Under the `#s3_client.copy_object` line, enter the following:

    `s3_client.copy_object(Bucket=s3_bucket,    Key=f'{output_loc}/{base_audio_key}',    CopySource={'Bucket': s3_bucket, 'Key': s3_audio_key}) `

15. Under the previous lines of code, enter the following:

    ```s3_client.copy_object(Bucket=s3_bucket,    Key=f'{output_loc}/{base_transcript_key},    CopySource={'Bucket': s3_bucket, 'Key': s3_transcript_key}) `

16. Under the `#s3_client.delete_objects` line, enter the following:

    ```
    deletes = {'Objects': [{'Key': s3_audio_key}, {'Key': s3_transcript_key}]}
    s3_client.delete_objects(Bucket=s3_bucket, Delete=deletes)
    ```

1. Click **Deploy**.
2. If you want, you can add another environment variable. Under *Environment Variables*, click **Edit**.
3. Click **Add environmental variable**.
4. Under *Key*, enter "KEYWORDS", and under *Value*, enter "important_supersecret".
5. Click **Save**.

### Categorize Audio Data

1. Return to the browser window or tab with the S3 Bucket console.
2. Click **Create a folder**.
3. Under *Folder name*, name the folder "upload".
4. Click **Create folder**.
5. Click the **upload/** folder.
6. Click **Upload**.
7. Click **Add files**.
8. Select an mp3 file to upload. You can find the `ImportantBusiness.mp3` file in the GitHub repository provided in the lab instructions.
9. Click **Upload**.
10. Under *Destination*, click the bucket name.
11. Return to the browser window or tab with the Step Function console. The step function should now be running.
12. Click on the step function name.
13. Click **Step input** to view the input.
14. Click **Step output** to view the output of the step function.
15. Return to the S3 Bucket console.
16. Click on the **meeting-audio-...** link.
17. Click the Refresh button in the console.
18. Click the **important/** folder.
19. Click the year, month, and day folder and confirm the MP3 and transcript files are saved correctly.
20. Return to the browser window or tab with the Step Function open.
21. Scroll down the page to view the execution event history