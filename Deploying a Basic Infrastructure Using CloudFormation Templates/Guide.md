# Deploy a Basic Infrastructure Using CloudFormation Templates

## Introduction

Your development team has been using this template for the intern-testing program. After performing an analysis, your team has determined that the `t3.small` instance was more compute power than they needed. Update the template so that the default instance defined in the stack is a `t3.micro`.

In this hands-on lab, we're going to jump into an environment that already has a CloudFormation stack deployed. We'll review the contents of the CloudFormation template, and then we'll perform direct updates to the stack itself.



## Solution

Log in to the AWS Management Console using the credentials provided on the lab instructions page. Make sure you're using the *us-east-1* region.



### Using CloudFormation Designer, Configure the InstanceType Stack Parameter to T3.Micro

1. In the search bar at the top, enter "CloudFormation".

2. Select **CloudFormation** from the dropdown menu.

3. Select the stack already in the CloudFormation dashboard.

4. Review the *Stack info* tab.

5. Review the *Events* tab (the newest events will appear first).

6. Review the *Resources* tab.

7. Right-click and open the physical ID for the *InternetGateway* in a new tab.

8. Right-click and open the physical ID for the *WebServerInstance* in a new tab.

9. Close out the *InternetGateway* and *WebServerInstance* tabs after reviewing.

10. Review the *Outputs* tab.

11. Right-click on the *PublicDNS* link and open it in a new tab. (Make sure to specify http, not https).

12. Navigate back to the CloudFormation dashboard.

13. Click on the *Parameters* tab.

14. Near the top of the page, next to **Delete**, click **Update**.

15. Ensure **Use current template** is selected and click **Next**.

16. Under InstanceType, select t3.micro.

    > **Note**: This only changes the current deployment of the stack.

17. Click **Cancel**.

18. Navigate back to the CloudFormation dashboard and click on the existing stack.

19. Click **Update** again.

20. Select **Edit template in designer** and click **View in Designer**.

21. Ensure `YAML` is selected for the template.

22. Under `Parameters`, change the `default` size from `t3.small` to `t3.micro` by erasing "small" and typing "micro".



### Launch the Updated Stack and Verify the New EC2 Resource Is Reachable

1. Copy the template and click on the checkmarked box icon in the top-left corner to validate the template. You should see *Template is valid*.

2. Click on the cloud icon next to the checkmarked box to launch the stack.

    > **Note**: This is a direct update to the existing stack.

3. Click **Next**.

4. Under *Parameters*, select the *InstanceType* dropdown box and select **t3.micro**.

5. Click **Next** through *Tags*.

6. Scroll down and select the acknowledgement under *Capabiities*.

7. Click **Update stack**.

8. Click on the refresh icon in the top-right corner of the CloudFormation dashboard to ensure the update is complete (this may take a few minutes).

9. Navigate to the *Resources* tab and open the *WebServerInstance* physical ID in a new tab to verify that the InstanceType is `t3.micro`.

10. Navigate back to the CloudFormation dashboard and select the *Outputs* tab.

11. Open the *PublicDNS* value in a new tab to ensure the instance is reachable via the public web



## Additional Resources
[AWS CloudFormation templates](https://github.com/awslabs/aws-cloudformation-templates/tree/master/aws/services)ates