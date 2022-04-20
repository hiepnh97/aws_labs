# Using Elasticache to Improve DynamoDB Performance

## Introduction

The AWS Training Architect Tournament site has become very popular within A Cloud Guru. Unfortunately, this means that operating the site has become prohibitively expensive. The backing table has had its read capacity units set to 1, and you've been instructed not to change it. On the other hand, you got permission to create a small ElastiCache cluster to implement a caching scheme that restores functionality to the site and generally improves performance. This will also reduce the monthly cost of running the site.

## Solution

1. Log in to the AWS Managment Console using the lab-provided credentials. Make sure you're in the `us-east-1` (N. Virginia) region.
2. Once logged in, open a new browser window and navigate to the [AWS Training Architect Tournament site](http://814917293444-tatourney.s3-website-us-east-1.amazonaws.com/).
3. On the tournament site, note the pizza images. These indicate that your scan operation is being throttled by the Lambda function. You can fix this with caching.

> **Note:** The code used for the solution in this lab can be [found on GitHub](https://github.com/linuxacademy/content-dynamodb-deepdive/tree/master/labs/solutions/UsingElastiCachetoImproveDynamoDBPerformance).

### Launch an ElastiCache Cluster

1. Navigate to ElastiCache.

2. Click **Get Started Now**.

3. Under **Cluster Engine**, select **Memcached**.

4. In **Name**, enter *tatourneycache*.

5. Set the *Node type* to **t2** and choose **cache.t2.small**.

6. Scroll down to **Advanced Memcached settings**.

7. In **Name** and **Description**, enter *tatourney*.

8. Under **Subnets**, select the available subnet.

9. Click Create.

    > **Note:** This will take 5 to 10 minutes to start up.

10. Once running, click the link under **Configuration Endpoint** and copy the node endpoints URL to a text file for later use.

11. Remove the colon and port number from the URL.

12. Click **Close**.

### Modify the getTaStats Lambda Function

1. Navigate to Lambda.

2. Select the function with *getTaStats* in its name.

3. Scroll down to **Code Source**.

4. Select the `editme.py` file.

5. In the `editme.py` code window, delete the pre-existing code.

6. Paste in the follow function code to implement read-through data caching:

    `from curtain import scanTable, deserialize from pymemcache.client import base import json def getStats():    endpoint = 'EndpointURL'    memClient = base.Client((endpoint, 11211))    data = []     items = memClient.get('scan')    if items is None:        items = scanTable()        while len(items) < 2:            items = scanTable()         data = deserialize(items)         memClient.set('scan', json.dumps(data))    else:        data = json.loads(items.decode())     ordered = sorted(data, key = lambda i: i['wins'], reverse=True)    return ordered `

7. On the line `endpoint = 'EndpointURL'`, replace `EndpointURL` with the previously copied URL.

8. Above the function, click **Deploy**.

#### Configure Additional Network Settings

1. Above **Code Source**, click **Configuration** .

2. From the left menu, click **VPC**.

3. Under **No VPC configuration**, click **Edit**.

4. Set the following values:

    - **VPC:** Default VPC
    - **Subnets:** Default subnet
    - **Security groups:** Default security group

5. Click Save.

    > **Note:** It may take a few minutes for the function to update.

6. Once updated, select the **Code** tab.

7. Scroll down to **Code Source** and click **Deploy**.

### Modify the taStreamProcessor Lambda Function

1. In Lambda, navigate back to the Functions page.

2. Select the function with *taStreamProcessor* in its name.

3. Scroll down to **Code Source**.

4. Select the `editme.py` file.

5. In the `editme.py` code window, delete the pre-existing code.

6. Paste in the follow function code to implement cache invalidation when records update:

    `from pymemcache.client import base def invalidateCache():    endpoint = 'EndpointURL'     memClient = base.Client((endpoint, 11211))    print('Invalidating Cache!')    memClient.delete('scan') `

7. On the line `endpoint = 'EndpointURL'`, replace `EndpointURL` with the previously copied URL.

8. Above the function, click **Deploy**.

#### Configure Additional Network Settings

1. Above **Code Source**, click **Configuration** .

2. From the left menu, click **VPC**.

3. Under **No VPC configuration**, click **Edit**.

4. Set the following values:

    - **VPC:** Default VPC
    - **Subnets:** Default subnet
    - **Security groups:** Default security group

5. Click Save.

    > **Note:** It may take a few minutes for the function to update.

6. Once updated, select the **Code** tab.

7. Scroll down to **Code Source** and click **Deploy**.

## Testing



1. Access to http://486726484754-tatourney.s3-website-us-east-1.amazonaws.com/
    1. Get link from tab `properties` of S3 bucket
2. Check the metrics of database(DynamoDB service)
3. Check metrics of ElastiCache Service
