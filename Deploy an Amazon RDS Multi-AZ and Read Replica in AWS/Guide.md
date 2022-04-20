# Deploying an Amazon RDS Multi-AZ and Read Replica

## Introduction

In this hands-on lab, we will work with Relational Database Service (RDS). This lab will provide you with hands-on experience with:

- Enabling Multi-AZ and backups
- Creating a read replica
- Promoting a read replica
- Updating the RDS endpoint in Route 53

Multi-AZ is strictly for failover, as the standby instances cannot be read from by an application. Read replicas are used for improved performance and migrations. With read replicas, you can write to the primary database and read from the read replica. Because a read replica can be promoted to be the primary database, it makes for a great tool in disaster recovery and migrations.

## Solution

Log in to the live AWS environment using the credentials provided. Make sure you're in the N. Virginia (`us-east-1`) region throughout the lab.

### Enable Multi-AZ Deployment

1. Navigate to **EC2** > **Load Balancers**.
2. Copy the DNS name of the load balancer.
3. Open a new browser tab, and enter the DNS name.
    - We will use this web page to test failovers and promotions in this lab.
4. Back in the AWS console, navigate to **RDS** > **Databases**.
5. Click on our database instance.
6. Click **Modify**.
7. Under *Multi-AZ deployment*, click **Create a standby instance (recommended for production usage)**.
8. Use a burstable class `db.t3.micro` instance.
9. Click **continue** at the bottom of the page.
10. Under *Scheduling of modifications*, select **Apply immediately**, and then click **Modify DB Instance**.
11. Once the instance shows Multi-AZ status as **Available** (it could take about 10 minutes), select the database instance.
12. Click **Actions** > **Reboot**.
13. On the reboot page, select **Reboot With Failover?**, and click **Confirm**.

### Create a Read Replica

1. With the database instance still selected, click **Actions** > **Create read replica**.
2. For *Destination region*, select **US East (N. Virginia)**.
3. In the *Settings* section, under *DB instance identifier*, enter "wordpress-rr".
4. Leave the other defaults, and click **Create read replica**. It will take a few minutes for it to become available.
5. Refresh the web page we navigated to earlier to see if our application is still there. It should be fine.

### Promote the Read Replica and Change the CNAME Records Set in Route 53 to the New Endpoint

1. Once the read replica is available, check the circle next to it.
2. Click **Actions** > **Promote**.
3. Leave the defaults, and click **Continue**, and then click **Promote Read Replica**.
4. Use the web page to monitor for downtime.
5. Once the read replica is available, click to view it.
6. In the *Connectivity & security* section, copy the endpoint.
7. Navigate to **Route 53** > **Hosted zones**.
8. Select the private hosted zone.
9. Select the **db.mydomain.local** record.
10. Click **Edit**.
11. Leave the *Record name* as **db**.
12. Replace what's currently in the *Value* box with the endpoint you copied.
13. Set the TTL to 60 seconds.
14. Click **Save changes**.
15. Monitor using the web page for downtime. (There shouldn't be any.)