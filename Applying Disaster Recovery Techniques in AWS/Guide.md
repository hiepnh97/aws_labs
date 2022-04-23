# Applying Disaster Recovery Techniques in AWS

## Introduction

In this hands-on lab, we will use a CloudFormation template to tackle stack recreation and get a chance to dive further into disaster recovery techniques through AWS.

## Solution

Log in to the AWS live environment using the `cloud_user` credentials provided. Make sure you are working in the `us-east-1` (N. Virginia) region.

Download the *amilookup.zip* and *AMILook.json* files we'll need later, which are provided on the [lab GitHub page](https://github.com/natonic/AWS_SA_Pro/blob/master/DR/amilookup.zip).

### Create a CloudFormation Stack

#### Create the Stack

1. Navigate to S3 using the *Services* menu or the unified search bar.
2. Click to open the provided bucket.
3. Check the checkbox next to either of the *CF_WordPress_Blog* provided templates.
4. Click **Copy URL** to copy a link to the bucket.
5. In a separate browser tab, navigate to EC2 using the *Services* menu or the unified search bar.
6. Select **Key Pairs** in the sidebar menu.
7. Create the key pair:
    - Click **Create Key Pair**.
    - In the *Key pair name* field, enter `drkeypair`.
    - Click **Create**.
8. Navigate to CloudFormation using the *Services* menu or the unified search bar.
9. Use the *Create stack* dropdown on the right to select **With new resources (standard)**.
10. Select **Amazon S3 URL** and paste your copied *Link* URL in the corresponding text field.
11. Click **Next**.
12. In the *Stack name* field, enter `drscenario`.
13. On the stack details page, set the following values:
    - *Stack name*: `drscenario`
    - *WebServerKeyName*: `drkeypair`
14. Click **Next**.
15. On the stack options page, leave the settings and click **Next**.
16. On the review page, click **Create stack**.

#### (Optional) Review Your Resources

1. While the CloudFormation stack is being created, you can open your *CF_WordPress_Blog* file and review it.
2. After the CloudFormation stack is finished creating, navigate to VPC using the *Services* menu or the unified search bar.
3. Use the sidebar menu to review your resources:
    - Select the **Subnets** link to review the 4 provided subnets.
    - Select the **Route Tables** link to review the provided route tables.
    - Select the **Internet Gateway** link to review the provided gateway details.
    - Select the **NAT Gateways** link to review the provided gateway details.
    - Select the **Network ACLs** link to review the provided network ACLs.
    - Select the **Security Groups** link to review the provided security groups.
4. Navigate to EC2 using the *Services* menu or the unified search bar.
5. Select the **Instances** link to review the provided instances. You should see 3 WordPress instances and 1 bastion host.
6. Select the **Auto Scaling Groups** link to review the provided Auto Scaling group details.
7. Select the **Launch configurations** link to review the provided launch configuration.

### Create a Cross-Stack Reference

#### Delete the Existing DR Stack

1. In a new browser tab, navigate to S3 using the *Services* menu or the unified search bar.
2. Click to open the provided bucket.
3. Click **Upload** and select the *amilookup.zip* file you downloaded at the beginning of the lab.
4. Leave all default settings and click **Upload**.
5. Open the *amilookup.zip* file to review the code.
6. Navigate back to the CloudFormation console, then select the stack provided for the lab and click **Delete**.
7. In the confirmation dialog box, click **Delete stack**. It will take a few minutes for the stack to be fully deleted.

#### Re-Create the WordPress Stack Using a Template

1. Use the *Create stack* dropdown to select **With new resources (standard)**.
2. In the *Prerequisite - Prepare template* section, select **Create template in Designer**.
3. Click **Create template in designer**.
4. Click the *Template* tab at the bottom of the page.
5. Copy everything in the *CF_WordPress_Blog_Revised.json* file from the [lab GitHub page](https://raw.githubusercontent.com/natonic/AWS_SA_Pro/master/DR/CF_WordPress_Blog_Revised.json) and paste it into the *Template* window.
6. Check the checkbox at the top to validate the template, then click the cloud icon with the up arrow to create the stack.
7. Click **Next**.
8. On the stack details page, set the following values:
    - *Stack name*: **DRStack**
    - *WebServerKeyName*: **drkeypair**
9. Click **Next**.
10. On the stack options page, leave the settings as is and click **Next**.
11. On the review page, click **Create stack**. It will take a few minutes to finish being created.

#### Create Another Stack Using a Different Template

1. Back in the S3 console, upload the *AMILook.json* file you downloaded at the beginning of the lab to our S3 bucket.
2. Copy the bucket name and paste it into a text file as well, since we'll need that in a minute.
3. Back in the CloudFormation console, use the *Create stack* dropdown to select **With new resources (standard)**.
4. Select **Upload a template file** and upload the *AMILook.json* file.
5. Click **Next**.
6. On the stack details page, set the following values:
    - *Stack name*: **amilookup**
    - *InstanceType*: **t2.micro**
    - *ModuleName*: **amilookup**
    - *S3Bucket*: Paste in the bucket name you copied earlier
    - *S3Key*: **amilookup.zip**
7. Click **Next**.
8. On the stack options page, leave the settings as is and click **Next**.
9. On the review page, check the box stating *I acknowledge that AWS CloudFormation might create IAM resources*.
10. Click **Create stack**. It will take a few minutes to be fully created.
11. Verify further by navigating to **EC2** and selecting **Instances**. You should see the new instance that was created.
12. Check the checkbox on the left-hand side of your new instance to view more details on the **Description** tab.