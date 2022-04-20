# Installing Terraform and Working With Terraform Providers

## Introduction

In this hands-on lab, we'll go through installing and configuring Terraform version 13 on a Linux OS. We will also explore how to select and use a Terraform provider from among the many providers available publicly.

## Solution

1. Log in to the lab server using the credentials provided:

    ```ssh cloud_user@<PublicIP> ```

2. In a web browser, log in to the AWS Management Console using the credentials provided.

### Download And Manually Install the Terraform Binary

1. Download the appropriate Terraform binary package for the provided lab server VM (Linux 64-bit) using the `wget` command:

    ```wget -c https://releases.hashicorp.com/terraform/0.13.4/terraform_0.13.4_linux_amd64.zip ```

2. Unzip the downloaded file:

    `unzip terraform_0.13.4_linux_amd64.zip `

3. Place the Terraform binary in the `PATH` of the VM operating system so the binary is accessible system-wide to all users:

    `sudo mv terraform /usr/sbin/ `

    > **Note:** If prompted, enter the username and password provided for the lab server.

4. Check the Terraform version information:

    `terraform version `

    Since the Terraform version is returned, you have validated that the Terraform binary is installed and working properly.

### Clone Over Code for Terraform Providers

1. Create a `providers` directory:

    `mkdir providers `

2. Move into the `providers` directory:

    `cd providers/ `

3. Create the file `main.tf`:

    `vim main.tf `

4. Paste in the following code from the provided [GitHub repo](https://github.com/linuxacademy/content-hashicorp-certified-terraform-associate-foundations/blob/master/section3-hol1/main.tf):

    `provider "aws" {  alias  = "us-east-1"  region = "us-east-1" } provider "aws" {  alias  = "us-west-2"  region = "us-west-2" }  resource "aws_sns_topic" "topic-us-east" {  provider = aws.us-east-1  name     = "topic-us-east" } resource "aws_sns_topic" "topic-us-west" {  provider = aws.us-west-2  name     = "topic-us-west" } `

5. To save and exit the file, press **Escape** and enter `:wq`.

### Deploy the Code with Terraform Apply

1. Enable verbose output logging for Terraform commands using `TF_LOG=TRACE`:

    `export TF_LOG=TRACE `

    > **Note:** You can turn off verbose logging at any time using the `export TF_LOG=` command.

2. Initialize the working directory where the code is located:

    `terraform init `

3. Review the actions performed when you deploy the Terraform code:

    `terraform plan `

    > **Note:** Two resources will be created, consistent with the providers that were configured in the provided code snippet.

4. Deploy the code:

    `terraform apply `

5. When prompted, type `yes` and press **Enter**.

6. Verify that two resources were created with their corresponding Amazon Resource Name (ARN) IDs in the region in which they were spun up.

7. Optionally, verify that the resources were created in their respective regions within the AWS Management Console:

    - Navigate to the AWS Management Console in your browser.
    - Verify that you are logged in to the *us-east-1* region upon signing in.
    - Click **Services**.
    - Type *SNS* in the search bar and select **Simple Notification Service** from the contextual menu.
    - In the menu on the left, click **Topics**.
    - Verify that the *topic-us-east* resource appears in the list.
    - At the top-right, click **N. Virginia** and select **us-west-2**.
    - Verify that the *topic-us-west* resource appears in the list.

8. Tear down the infrastructure you just created before moving on:

    `terraform destroy --auto-approve `

## Conclusion

Congratulations — you've completed this hands-on lab!