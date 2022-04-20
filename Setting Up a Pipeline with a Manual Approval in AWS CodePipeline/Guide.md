# Setting Up an AWS CodePipeline with a Manual Approval

## Introduction

AWS CodePipeline is a native AWS solution that provides a continuous integration and continuous deployment pipeline offering to its clients. In this hands-on lab, we will implement AWS CodePipeline to deploy AWS infrastructure through AWS CloudFormation. We will add an action to our AWS CodePipeline that requires a manual approval intended to have any code commits reviewed prior to being deployed.

## Solution

Log in to the live AWS environment using the credentials provided. Make sure you're in the N. Virginia (`us-east-1`) region throughout the lab.

Download the file needed for this lab at the [lab GitHub page](https://github.com/natonic/Developer-Tools-Deep-Dive/tree/master/Labs/CodePipelineWithManualApproval).

### Create an AWS IAM Role

1. From the AWS console, navigate to Identity and Access Management (IAM).
2. Click **Roles** in the left-hand menu.
3. Click **Create role**.
4. Select **CloudFormation** as the service that will use this role.
5. Click **Next: Permissions**.
6. Select the checkbox for the `AdministratorAccess` permissions policy.
7. Click **Next: Tags**.
8. Click **Next: Review**.
9. Enter *pipelineperms4CF* as the role name.
10. Click **Create role**.

### Create an AWS CodeCommit Repository and SNS Topic

1. From the AWS console, navigate to CodeCommit and click **Create repository**.
2. Enter *pipeline4cf* as the repository name.
3. Click **Create**.
4. In a new browser tab or window, navigate to the [lab GitHub page](https://github.com/natonic/Developer-Tools-Deep-Dive/tree/master/Labs/CodePipelineWithManualApproval).
5. Click **Raw**.
6. Select all content from the raw file, and then copy and paste into a new local file on your computer. Save the file as `S3Retain.yaml`.
7. Click **Add file**.
8. Click **Upload file**.
9. Click **Choose file**.
10. Select the `S3Retain.yaml` file that was saved to your local computer.
11. Enter your name as the author name.
12. Enter your email address as the email address.
13. Click **Commit changes**.
14. Navigate to Simple Notification Service (SNS).
15. In the *Create topic* box on the main SNS page, enter *manualapprove* as the topic name. (Standard version)
16. Click **Next step**.
17. Accept the defaults on the next page by clicking **Create topic**.
18. Click **Create subscription**.
19. Choose **Email** as the protocol.
20. Enter your email address as the endpoint.
21. Click **Create subscription**.
22. Navigate to your inbox, open the `AWS Notification - Subscription Confirmation` message, and click the **Confirm subscription** link.

### Create an AWS CodePipeline Pipeline

1. Navigate to the CodePipeline console.

2. Click **Create pipeline**.

3. Enter *ManualApprovalPipeline* as the pipeline name.

4. Ensure **New service role** is selected.

5. Ensure **Allow AWS CodePipeline to create service role so it can be used with this new pipeline** is checked.

6. Expand the *Advanced settings* section and ensure the **Default location** and **Default AWS Managed Key** options are selected.

7. Click **Next**.

8. On the Add source stage page, set the following values:

    - *Source provider*: **AWS CodeCommit**
    - *Repository name*: **pipeline4cf**
    - *Branch name*: **main**
    - *Change detection options*: **Amazon CloudWatch Events (recommended)**

9. Click **Next**.

10. Click **Skip build stage**.

11. Click **Skip**.

12. On the Add deploy stage page, set the following values:

    - *Deploy provider*: **AWS CloudFormation**
    - *Region*: **US East - (N. Virginia)**
    - *Action mode*: **Create or update a stack**
    - *Stack name*: **s3bucketretain**
    - *Artifact name*: **SourceArtifact**
    - *File name*: **S3Retain.yaml**
    - *Role name*: **pipelineperms4CF**

13. Click **Next** > **Create pipeline**.

14. Click the **AWS CloudFormation** link in the **Deploy** panel.

15. Once CloudFormation shows complete, return to the CodePipeline service.

16. Verify the `manualapprove` pipeline status shows `Succeeded` in the **Deploy** panel.

17. Select our pipeline.

18. Click **Edit**.

19. Click **+ Add stage** between the **Source** and **Deploy** panels.

20. Enter *manualapproval* as the stage name and click **Add stage**.

21. Click **+ Add action group**.

22. In the Edit action dialog box, set the following values:

    - *Action name*: **manualapproval**
    - *Action provider*: **Manual approval**
    - *SNS topic ARN*: Select the listed SNS topic ARN we created earlier

23. Click **Done** > **Save** > **Save**.

24. Click **Release change** to restart the pipeline.

25. Click **Release**.

26. Navigate to your inbox, and open the `APPROVAL NEEDED...` message to see what your team would receive in a real-world environment.

27. Navigate back to CodePipeline.

28. Click **Review** in the *Manual approve* panel.

29. Enter *Looks good — approved.* in the comments, and click **Approve**.
