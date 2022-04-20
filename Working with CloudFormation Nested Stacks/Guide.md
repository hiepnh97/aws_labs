# Working with CloudFormation Nested Stacks

## Introduction

In this hands-on lab, we will create a nested stack from the templates provided. We will use the two templates to create a nested stack that will implement a child template, which will then create an S3 bucket with a policy of no retain. This child template can be reused repeatedly whenever an S3 bucket of this type is needed.

## Solution

Log in with the credentials provided, and make sure you are in the `us-east-1` (N. Virginia) region.

Download the necessary files from the lab's [GitHub repository](https://github.com/natonic/CloudFormation-Deep-Dive/tree/master/Labs/NestedStacks).

### Create an S3 Bucket and Upload a CloudFormation Template to It

1. Navigate to S3.
2. Click **+ Create bucket**.
3. On the *Name and region* screen, give your bucket a unique name. (**Note:** It must be all lowercase letters and be unique across *all* AWS accounts.)
4. Click **Next**.
5. Accept the default settings on the next screens, and click **Create bucket**.
6. Click to open the bucket, and click **Upload**.
7. Click **Add files**, and select the `s3static.json` CloudFormation template you downloaded earlier.
8. Accept the default settings on the next screens, and click **Upload**.
9. Click **Upload**.
10. Click **Add files**, and select the `noretain.json` CloudFormation template you downloaded earlier.
11. Accept the default settings on the next screens, and click **Upload**.

### Create a Nested Stack from the CloudFormation Root Template

1. In a new browser tab, navigate to CloudFormation.

2. Click **Create stack**.

3. In the *Prerequisite - Prepare template* section, select **Create template in Designer**.

4. Click **Create template in designer**.

5. Click the *Template* tab at the bottom.

6. Paste the following (the `root.json` template included in the lab GitHub) into the *Template* window:

```
{
    "AWSTemplateFormatVersion" : "2010-09-09",
    "Resources" : {
        "myStack" : {
	       "Type" : "AWS::CloudFormation::Stack",
	       "Properties" : {
              "TemplateURL" : "https://s3.amazonaws.com/<YOUR-BUCKET-NAME>/noretain.json",
              "TimeoutInMinutes" : "60"
	       }
        }
    }
}
```

7. In the `"TemplateURL"` line, replace `<YOUR-BUCKET-NAME>` with the name of the bucket you just created.

8. Click the checkbox at the top to validate the template, and then click the cloud icon with the up arrow to create the stack.

9. Click **Next**.

10. On the stack details page, give it a *Stack name* of **s3webnoretain**.

11. Click **Next**.

12. Leave the settings on the stack options page, and click **Next**.

13. Check the boxes to accept the acknowledgements, and click **Create stack**. It will take a few minutes for it to fully be created.

### Create a Nested Stack with Multiple Child Stacks

1. In the CloudFormation browser tab, click **Create stack**.

2. In the *Prerequisite - Prepare template* section, select **Template is ready**.

3. Click **Upload a template file**.

4. Click **Choose file**.

5. Select the `multinest.json` template, which is included in the lab GitHub repository.

6. Click **View in Designer**.

```
{
    "AWSTemplateFormatVersion" : "2010-09-09",
    "Resources" : {
        "myStack" : {
	       "Type" : "AWS::CloudFormation::Stack",
	       "Properties" : {
              "TemplateURL" : "https://s3.amazonaws.com/<YOUR-BUCKET-NAME>/s3static.json",
              "TimeoutInMinutes" : "60"
	       }
        },
        "myStack2" : {
            "Type" : "AWS::CloudFormation::Stack",
            "Properties" : {
               "TemplateURL" : "https://s3.amazonaws.com/<YOUR-BUCKET-NAME>/noretain.json",
               "TimeoutInMinutes" : "60"
            }
         }    
    }
}
```

7. In the `"TemplateURL"` lines, replace `<YOUR-BUCKET-NAME>` with the name of your bucket.

8. Click the checkbox at the top to validate the template, and then click the cloud icon with the up arrow to create the stack.

9. Click **Next**.

10. On the stack details page, give it a *Stack name* of **twochildrenstacks**.

11. Click **Next**.

12. Leave the settings on the stack options page, and click **Next**.

13. Check the boxes to accept the acknowledgements, and click **Create stack**. It will take a few minutes for it to fully be created.

### Upload an `index.html` File and Browse to It

1. In the S3 browser tab, click to open one of the nested stack buckets.
2. Click **Upload**.
3. Click **Add files**, and select the `index.html` file included in the lab GitHub repository.
4. Accept the default settings on the next screens, and click **Upload**.
5. Click **Upload**.
6. In the CloudFormation browser tab, select the nested stack in which you uploaded the `index.html` file.
7. Click the **Outputs** tab, and browse to the listed *WebsiteURL*. It should display an Elastic Beanstalk web page, which is fine — all that matters is if it shows up alright.
