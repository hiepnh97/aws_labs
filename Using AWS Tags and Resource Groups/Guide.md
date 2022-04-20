
AMI: Amazon Machine Image
# Using AWS Tags and Resource Groups

## Introduction

To simplify the management of AWS resources such as EC2 instances, you can assign metadata using tags. Resource groups can then use these tags to automate tasks on large numbers of resources at one time. They serve as a unique identifier for custom automation, to break out cost reporting by department and much more. In this hands-on lab, we will explore tag restrictions and best practices for tagging strategies. We will also get experience with the Tag Editor, AWS resource group basics, and leveraging automation through the use of tags.

## Solution

Log in to the live AWS environment using the credentials provided. Make sure you're in the N. Virginia (`us-east-1`) Region throughout the lab.

### Set Up AWS Config

1. Navigate to *Config* using the *Services* menu or the unified search bar.
2. In the *Set up AWS Config* window, click **1-click setup**.
3. Leave the settings as their defaults.
4. Click **Confirm**.

### Tag an AMI and EC2 Instance

1. In a new browser tab, navigate to **EC2** > **Instances (running)**.

2. Select any one of the instances listed.

3. Right-click on the selected instance and select **Image and templates** > **Create image**.

4. For the *Image name*, enter "Base".

5. Click **Create image**.

6. Click **AMIs** in the left-hand menu.

7. Once the AMI you just created has a status of *available*, select it. (It could take up to 5 minutes.)

8. Click **Launch**.

9. Select *t3.micro*, and click **Next: Configure Instance Details**.

10. Leave the defaults on the *Configure Instance Details* page.

11. Click **Next: Add Storage**, and then click **Next: Add Tags**.

12. On the Add Tags page, click Add tag and set the following values:
    - *Key*: **Name**
    - *Value*: **Test Web Server**

13. Click **Next: Configure Security Group**.

14. Click **Select an existing security group**.

15. Select the one with **SecurityGroupWeb** in the name (*not* the default security group).

16. Click **Review and Launch**.

17. Click **Continue** in the warning dialog.

18. If the *Boot from General Purpose (SSD)* dialog pops up, click **Next**.

19. Click **Launch**.

20. In the key pair dialog, select **Proceed without a key pair** and check the acknowledgement box.

21. Click **Launch Instances**.

22. Click **View Instances**, and give it a few minutes to enter the *running* state.

### Tag Applications with the Tag Editor

#### Module 1 Tagging

1. Navigate to *Resource Groups & Tag Editor*.

2. Click **Tag Editor** in the left-hand menu.

3. In the *Find resources to tag* section, set the following values:
    - *Regions*: **us-east-1**
    - Resource types:
        - **AWS::EC2::Instance**
        - **AWS::S3::Bucket**

4. Click **Search resources**.

5. In the Resource search results section, set the following values:
    1. Enter "Mod. 1" in the *Filter resources* search window and press **Enter** to execute the search.
    2. Select **both** instances and click **Clear filters**.
    3. Enter "moduleone" in the *Filter resources* search window and press **Enter** to execute the search.
    4. Select the listed S3 bucket and click **Clear filters**.

6. Click **Manage tags of selected resources**.

7. In the Edit tags of all selected resources section, click `Add tag` and set the following values:
    - *Tag key*: **Module**
    - *Tag value*: **Starship Monitor**

8. Click **Review and apply tag changes** > **Apply changes to all selected**.

#### Module 2 Tagging

1. In the Find resources to tag section of the `Tag Editor` page, set the following values:
    - *Regions*: **us-east-1**
    - Resource types:
        - **AWS::EC2::Instance**
        - **AWS::S3::Bucket**

2. Click **Search resources**.

3. In the `Resource search results` section, set the following values:
    1. Enter "Mod. 2" in the *Filter resources* search window and press **Enter** to execute the search.
    2. Select **both** instances and click **Clear filters**.
    3. Enter "moduletwo" in the *Filter resources* search window and press **Enter** to execute the search.
    4. Select the S3 bucket click **Clear filters**.

4. Click **Manage tags of selected resources**.

5. In the Edit tags of all selected resources section, click Add tag and set the following values:
    - *Tag key*: **Module**
    - *Tag value*: **Warp Drive**

6. Click **Review and apply tag changes** > **Apply changes to all selected**.


### Create Resource Groups and Use AWS Config Rules for Compliance

#### Create the `Starship-Monitor` Resource Group

1. In the left-hand menu, select **Create Resource Group**.

2. Select **Tag based**.

3. In the *Grouping criteria* section, click **All supported resource types**.

4. In the *Tags* field, add the following:
    - *Tag key*: **Module**
    - *Optional tag value*: **Starship Monitor**

5. Click **Preview group resources**.

6. In the *Group Details* section, enter a *Group name* of "Starship-Monitor".

7. Click **Create group**.

#### Create the `Warp-Drive` Resource Group

1. In the left-hand menu, click **Create Resource Group**.

2. Select **Tag based**.

3. In the *Grouping criteria* section, click **All supported resource types**.

4. In the *Tags* field, add the following:
    - *Tag key*: **Module**
    - *Optional tag value*: **Warp Drive**

5. Click **Preview group resources**.

6. In the *Group Details* section, enter a *Group name* of "Warp-Drive".

7. Click **Create group**.

#### View the Saved Resource Groups

1. Click **Saved Resource Groups** in the left-hand menu.
2. Click **Starship-Monitor**. Here, we should see all the resources in our Starship-Monitor group.

#### Use AWS Config Rules for Compliance

1. Navigate to **EC2** > **Instances**.

2. Select the **Test Web Server** instance.

3. In the *Details* section, copy its AMI ID.

4. Navigate to your AWS Config Console tab.

5. In the left-hand menu, click **Rules**.

6. Click **Add rule**.

7. Select **Add AWS managed rule** for the rule type.

8. Search for "approved-amis-by-id" in the search box, and select that rule.

9. Click **Next**.

10. In the Trigger section, set the following values:
    - *Scope of changes*: **Tags**
    - Resources by tag:
        - *Tag key*: **Module**
        - *Tag value*: **Starship Monitor**

11. In the *Parameters* section, paste the AMI ID you copied earlier into the *Value* field.

12. Click **Next** > **Add rule**.

13. Back in the EC2 instances console, select all the instances.

14. Click **Instance state** > **Reboot instance**.

15. In the *Reboot instances* dialog, click **Reboot**.

16. Back in the AWS Config Console, after a few minutes, we should see there are now noncompliant resources.

17. Click the **approved-amis-by-id** link.

18. Click the link for one of the noncompliant resources to see more information.


Additional Resources

Your company runs many applications in a shared AWS account with hundreds of instances. The application and security teams want an easy way to find resources associated with a particular application. AWS tags and resource groups demonstrated in this lab make it easy to identify application components.

### Lab Prerequisites

- Understand how to log in to and use the AWS Management Console.
- Understand EC2 basics, including how to launch an instance.
- Understand AWS Identity & Access Management (IAM) basics, including users, policies, and roles.
- Understand how to use the AWS Command Line Interface (CLI).

### Helpful Documentation

- [Tag Editor](https://docs.aws.amazon.com/ARG/latest/userguide/tag-editor.html)
- [Tagging Strategies](https://aws.amazon.com/answers/account-management/aws-tagging-strategies/)
- [Tagging and Cost Allocation](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html#allocation-what)
- [AWS Resource Groups](https://docs.aws.amazon.com/ARG/latest/userguide/welcome.html)
- [AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)
- [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
