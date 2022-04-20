# Understanding CloudFormation Template Anatomy

## Introduction

This lab takes an in-depth look at CloudFormation template anatomy. Each section of a CloudFormation template will be covered in detail, and, ultimately, a CloudFormation template will be constructed piece by piece. After completing this lab, the student will have a deeper understanding of constructing CloudFormation templates in both JSON and YAML.

## Solution

Log in with the credentials provided, and make sure you are in the `us-east-1` (N. Virginia) region.

Download the templates used in the lab [here](https://github.com/natonic/CloudFormation-Deep-Dive/tree/master/Labs/TemplateAnatomy).

### Create a CloudFormation Stack

1. Navigate to CloudFormation.
2. Click **Create stack**.
3. In the new CloudFormation page, click *Designer*
4. Click the *Template* tab at the bottom.
5. Copy everything in the `Template_Anatomy2.yaml` file ([found on GitHub](https://raw.githubusercontent.com/natonic/CloudFormation-Deep-Dive/master/Labs/TemplateAnatomy/Template_Anatomy2.yaml)), and paste it into the *Template* window.
6. In a new browser tab, navigate to **EC2** > **Key Pairs**.
7. Click **Create Key Pair**.
8. Give it a key pair name of "tempanatomy", and click **Create**.
9. Click **Security Groups** in the left-hand menu.
10. Copy the security group ID and paste it into a text file, since we'll need it in a minute.
11. Navigate to **VPC** > **Subnets**.
12. Select one of the listed subnets, and copy its subnet ID. Paste it into a text file, since we'll also need it later.
13. Back in the CloudFormation template window, click the checkbox at the top to validate the template, and then click the cloud icon with the up arrow to create the stack.
14. Click **Next**.
15. On the stack details page, set the following values:
    - *Stack name*: **tempanatomyLab**
    - *InstanceType*: **t2.micro**
    - *KeyName*: **tempanatomy**
    - *MySG*: Paste in the security group ID you copied earlier
    - *MySubnet*: Paste in the subnet ID you copied earlier
16. Click **Next**.
17. On the stack options page, set the *Key* as "name" and *Value* as "tempanatomy".
18. Click **Next**.
19. Click **Create stack**. It will take a few minutes for it to fully be created.

### Delete a CloudFormation Stack

1. Once it's created, click **Delete** at the top.
2. In the confirmation dialog, click **Delete stack**.
3. Monitor the deletion process by watching the *Events* tab.

# NOTE:
Security group ID: sg-021346861c7d1aab5
Subnet ID: subnet-06aed50c6af6253c4