# Using CloudWatch for Resource Monitoring

## Introduction

Welcome to this AWS hands-on lab for Using CloudWatch for Resource Monitoring!

This lab provides practical experience with creating and configuring multiple custom AWS CloudWatch dashboards and widgets.

The primary focus will be on the following features within CloudWatch:

1. CloudWatch Dashboards
2. Dashboard Widgets
3. CloudWatch Metrics

## Solution

1. Log in to the AWS Management Console using the credentials provided on the lab instructions page. Make sure you're using the `us-east-1` region.

### Create a CloudWatch Dashboard for the DMZ Layer

1. In the AWS Management Console, start typing "CloudWatch" into the search box and click on **CloudWatch** when it appears in the list.

2. Click on **Dashboards** from the left-hand menu.

3. Click **Create dashboard**.

4. Under *Dashboard name:* enter "DMZLayer".

5. Click **Create dashboard**.

6. Select the **Line** option and click **Next**.

7. Select **Metrics** and click **Configure**.

8. Under *All Metrics*, select **EC2**.

9. Click **Per-Instance Metrics**.

10. In the filter box, enter "CPUUtilization".

11. Select the box next to **bastion-host**.

12. Click on **custom** at the top of the window and select **15 Minutes**.

13. Click **Create widget**.

14. Click **Save dashboard**.

    > Note: If 2 load balancers are present, select the load balancer with 0 as **RequestCount**.

### Create a CloudWatch Dashboard for the Application Layer

1. Click on **Metrics** from the left-hand menu.
2. Click **EC2**.
3. Click **Per-Instance Metrics**.
4. Find *CPUUtilization* under *Metric Name* and click the down arrow next to the name. Select **Search for this only** from the menu.
5. Select the **database** instance and both **instance-wordpress** instances by clicking the boxes next to their names.
6. Click on **custom** at the top of the window and select **15 Minutes**.
7. Click the dropdown at the top with the word **Line** displayed. Select **Stacked area** from the list of options.
8. Click **Actions** in the top-right corner and select **Add to dashboard**.
9. Click **Create new** under **Select a dashboard**. Enter "AppLayer" in the box that appears and then click the checkmark next to the box.
10. Click **Add to dashboard**.
11. Click **Add widget**.
12. Select **Number**.
13. Click **Next**.
14. Click **ApplicationELB**.
15. Click **Per AppELB Metrics**.
16. Find *RequestCount* under *Metric Name* and click the down arrow next to *RequestCount*. Select **Search for this only** from the menu. Checkmark your load balancer.
17. Click **Create widget**.
18. Click **Save dashboard**.
19. Click **Add widget**.
20. Select **Line**.
21. Select **Metrics**.
22. Click **Configure**.
23. Click **EC2**.
24. Click **Per-Instance Metrics**.
25. Find *NetworkIn* under *Metric Name* and click the down arrow next to *NetworkIn*. Select **Search for this only** from the menu.
26. Select the **database** instance and both **instance-wordpress** instances by clicking the boxes next to their names.
27. Click **Create widget**.

### Test the Widgets

1. Navigate back to the EC2 Management Console in a second browser tab.
2. Select **Load Balancers** in the left-hand menu.
3. Under *Description > Basic Configuration*, copy the *DNS name*.
4. Open a new tab and paste the load balancer DNS name.
5. For **English**, click **Continue**.
6. For *Site Title*, enter "Lab".
7. For *Username*, enter "wpuser".
8. For *Password*, enter "Password1".
9. Click the box for **Confirm use of weak password**.
10. For *Your Email*, enter "test@acloud.guru".
11. Click **Install WordPress**.
12. Click **Log In**.
13. Enter the credentials just created and log in to the site.
14. Navigate back to the CloudWatch Management Console tab.
15. Click on the refresh icon for the `CPUUtilization` box.
16. Click on the three dots in the top-right corner of the `CPUUtilization` box and select **Edit**.
17. Click **custom** at the top-right corner and then select **15 Minutes**.
18. To configure *Auto refresh*, click on the down arrow next to the refresh icon and select **10 Seconds** as the *Refresh interval*.
19. Click **Update widget**.
20. Click on the refresh icon for the `CPUUtilization` dashboard (this may take a few minutes). These values will show that you are now monitoring resources using CloudWatch.
