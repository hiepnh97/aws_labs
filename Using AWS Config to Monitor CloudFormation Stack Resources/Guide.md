# Using AWS Config to Monitor CloudFormation Stack Resources

## Introduction

In this hands-on lab, we will use AWS Config to monitor resources within an AWS environment. We will use a CloudFormation template to create an AWS Config rule to monitor the EC2 instances in an environment. The rule will detect whether instances launched in the environment comply with the instance types specified as accepted within the Config rule.

## Solution

Log in to the AWS environment using the credentials provided. Make sure you are using `us-east-1` (N. Virginia) as the selected region.

There are three templates for this lab, which you can download from the [lab's GitHub repository](https://github.com/natonic/CloudFormation-Deep-Dive/tree/master/Labs/CF with AWS Config).

### Create a Stack that Contains Three EC2 Instances

#### Create Stack

1. Navigate to CloudFormation.

2. Click **Create stack** > **With new resources (standard)**.

3. In the *Prerequisite - Prepare template* section, select **Create template in Designer**.

4. Click **Create template in designer**.

5. In the pane at the bottom of the screen, click the **Template** tab along the bottom.

6. Copy everything in the `badSG.json` file ([from the lab GitHub](https://raw.githubusercontent.com/natonic/CloudFormation-Deep-Dive/master/Labs/CF with AWS Config/badSG.json)), and paste it into the *Template* window.

7. Click the checkbox at the top to validate the template.

8. In a new browser tab, navigate to **EC2** > **Key Pairs**.

9. Click **Create key pair**.

10. Give it a key pair name of "configLab", and click **Create key pair**.

11. Back in the CloudFormation template browser tab, click the cloud icon with the up arrow at the top to create the stack.

12. Click **Next**.

13. On the stack details page, set the following values (
    for the last few values, navigate to their pages in the second browser tab you opened for EC2):

    - *Stack name*: **configLab**

    - *Instance1*: **t2.small**

    - *Instance2*: **t2.small**

    - *Instance3*: **t2.micro**

    - *KeyName*: **configLab**

    - MySG: Paste the value found here:

        1. Navigate to **EC2** > **Security Groups**.
        2. Copy the security group ID of the one pre-configured for the lab (**NOT** the default security group).

    - MySubnet: Paste the value found here:

        1. Navigate to **VPC** > **Subnets**.
        2. Select one of the listed subnets, and copy its subnet ID.

    - MyVPC: Paste the value found here:

        1. Navigate to **VPC** > **Your VPCs**.
        2. Copy the VPC ID.

14. Click **Next**.

15. Leave the defaults on the stack options page, and click **Next**.

16. Click **Create stack**. After a minute or so, we should see the stack creation fail (the errors will be related to our three EC2 instances).

#### Update Stack

1. Click the **Template** tab at the top.

2. Click **View in Designer**.

3. In the `Resources` block, for each instance object, change `SecurityGroups` to `SecurityGroupIds` . (It will be in three spots — one for each instance.)

    - You can make sure it matches by checking it against the `goodSG.json` file ([from the lab GitHub](https://raw.githubusercontent.com/natonic/CloudFormation-Deep-Dive/master/Labs/CF with AWS Config/goodSG.json)).

4. Click the checkbox at the top to validate the template, and then click the cloud icon with the up arrow to create the stack.

5. Click **Next**.

6. On the stack details page, set the following values:

    - *Stack name*: **configLab2**
    - *Instance1*: **t2.small**
    - *Instance2*: **t2.small**
    - *Instance3*: **t2.micro**
    - *KeyName*: **configLab**
    - *MySG*: The same value used for the original *configLab* stack
    - *MySubnet*: The same value used for the original *configLab* stack
    - *MyVPC*: The same value used for the original *configLab* stack

7. Click **Next**.

8. Leave the defaults on the stack options page, and click **Next**.

9. Click **Create stack**. This time, stack creation should be successful.

### Create Stack That Deploys an AWS Config Rule to Evaluate EC2 Instances

#### Create Stack

1. Click **Create stack** > **With new resources (standard)**.
2. Select **Create template in Designer**.
3. Click **Create template in designer**.
4. Click the *Template* tab at the very bottom.
5. Copy everything in the `awsconfigrule.json` file ([from the lab GitHub](https://raw.githubusercontent.com/natonic/CloudFormation-Deep-Dive/master/Labs/CF with AWS Config/awsconfigrule.json)), and paste it into the *Template* window.
6. Click the checkbox at the top to validate the template, and then click the cloud icon with the up arrow to create the stack.
7. Click **Next**.
8. On the stack details page, set the following values:
    - *Stack name*: **configrule**
    - *instanceType*: **t2.micro**
9. Click **Next**.
10. Leave the defaults on the stack options page, and click **Next**.
11. Click **Create stack**. After a minute or so, we should see the stack creation fail (the error will be due to a missing configuration recorder).
12. With the *configrule* stack selected, click **Delete**.
13. In the confirmation dialog that pops up, click **Delete stack**.
14. Select the *configLab* stack, and click **Delete**.
15. In the confirmation dialog that pops up, click **Delete stack**.

#### Set Up AWS Config

1. In another browser tab, navigate to Config.
2. Click **Get started**.
3. Set the following values:
    - *All resources*: Check the box to **Record all resources supported in this region**
    - *Amazon S3 bucket*: **Create a bucket**
    - *AWS Config role*: **Create AWS Config service-linked role**
4. Click **Next**.
5. On the *AWS Config rules* page, click **Next**.
6. On the *Review* page, click **Confirm**.
7. On the Config dashboard, click **Settings** in the left-hand menu.
8. Verify that recording is on.

#### Create Another Stack

1. Back in the CloudFormation browser tab, click **Create stack** > **With new resources (standard)**..

2. Select **Template is ready**.

3. Select **Upload a template file**.

4. Click **Choose file**, and upload the`awsconfigrule.json` file (which you can download from the [lab GitHub page](https://github.com/natonic/CloudFormation-Deep-Dive/blob/master/Labs/CF with AWS Config/awsconfigrule.json)).

5. Click **Next**.

6. On the stack details page, set the following values:

    - *Stack name*: **configrule**
    - *instanceType*: **t2.micro**

7. Click **Next**.

8. Leave the defaults on the stack options page, and click **Next**.

9. Click **Create stack**. After a few moments, the stack creation should succeed.

10. Head back to the AWS Config browser tab.

    > **Note:** If it still says *Taking inventory...*, you may need to turn recording off and then immediately turn it back on in order for that message to go away (it may take 10–15 seconds for it to disappear).

11. Click **Rules** in the left-hand menu. There, we should see it says there are two noncompliant resources.

12. Click the **desired-instance-type** rule name to view the noncompliant resources — it's our two instances that are `t2.small` instead of `t2.micro`.

### Make EC2 Instances Compliant with Config Rule

1. Back in CloudFormation, select our *configLab2* stack and click **Update**.
2. With **Use current template** selected, click **Next**.
3. Change *Instance1* and *Instance2* to **t2.micro**.
4. Click **Next**.
5. Leave the defaults on the stack options page, and click **Next**.
6. Click **Update stack**.
7. In another browser tab, navigate to **EC2** > **Instances**. We should see our two modified instances are updating.
8. Back in CloudFormation, check the stack status to make sure it updates alright.
9. Check the instances in EC2 to make sure they finished updating alright.
10. Back in AWS Config, click **Re-evaluate**. After 5–10 minutes, we should see all of our resources are now compliant.
