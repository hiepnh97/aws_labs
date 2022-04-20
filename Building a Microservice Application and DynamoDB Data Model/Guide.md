# Building a Microservice Application and DynamoDB Data Model

## Introduction

In this hands-on lab, we will be presented with a web front end that is ready to be connected to a data system back end. We will analyze the provided dataset, create a data model, create a DynamoDB table, and edit two Lambda functions to load data into the table we will create, and connect that table to an API to provide data to the website.

## Solution

Log in to the live AWS environment using the credentials provided. Make sure you're in the N. Virginia (`us-east-1`) region throughout the lab.

The code used in the solution videos for this lab can be found [here](https://github.com/linuxacademy/content-dynamodb-datamodeling/tree/master/labs/microservice/solution).

### Examine Source Data and Formulate Data Model

1. Download the `.csv` data files provided on the lab page.
2. Open each file and examine the source data.
3. Consider the best way to formulate the data model. (Watch the "Solution 1/4" video to see our process.)

### Create a DynamoDB Table

1. In the AWS console, navigate to **DynamoDB** > **Tables**.

2. Click

     

    Create table

    , and set the following values:

    - *Table name*: **collectors**
    - *Primary key*: **uid**

3. Check **Add sort key**.

4. In the sort key field that appears, enter "item_name".

5. Un-check **Use default settings**.

6. Click **+ Add index**.

7. In the

     

    Add index

     

    dialog, set the following values:

    - *Primary key*: **uid**
    - *Add sort key*: Check
    - In the field under *Add sort key*: **type**
    - *Index name*: **type-index**
    - *Create as Local Secondary Index*: Check

8. Click **Add index**.

9. Click **+ Add index**.

10. In the

     

    Add index

     

    dialog, set the following values:

    - *Primary key*: **uid**
    - *Add sort key*: Check
    - In the field under *Add sort key*: **date**
    - *Index name*: **date-index**
    - *Create as Local Secondary Index*: Check

11. Click **Add index**.

12. In the *Read/write capacity mode* section, check **On-demand**.

13. Click **Create**.

### Add Data Transformations/Mutations to `collectors_load` Lambda Function

1. Copy the entirety of the `collectors_load.py` file contents (which can be [found on GitHub](https://raw.githubusercontent.com/linuxacademy/content-dynamodb-datamodeling/master/labs/microservice/solution/collectors_load.py)).
2. Navigate to Lambda in a new browser tab.
3. Click **collectors_load**.
4. In the *Function code* section, delete the existing code for `tableload.py` and paste in the `collectors_load.py` [file contents](https://raw.githubusercontent.com/linuxacademy/content-dynamodb-datamodeling/master/labs/microservice/solution/collectors_load.py).
5. Click **Save**.
6. Navigate back to the DynamoDB page to make sure your table is created.

### Run `collectors_load` Function

1. Back on the *collectors_load* page, click in the *Select a test event* field, and click **Configure test events**.
2. Give it an *Event name* of "blank".
3. Click **Create**.
4. Click **Test**.
5. Expand the *Execution result: succeeded* section.
6. In the *Log output* results, make sure there are no unprocessed items listed.
7. Navigate back to the DynamoDB page, and click the **Items** tab.
8. Refresh it to make sure the items have populated.

#### Run Queries on the `collectors` Table

1. In the *Scan* field, select **Query** in the dropdown.
2. Enter a partition key string value of "john".
3. Click **Start search**. This will display all items with the `uid` of "john".
4. On the lab page, navigate to the provided Collectors User Profile site URL. For now, it should just be a simple site without much information.
5. Click the *[Table] collectors: uid, item_name* dropdown, and select **[Index] type-index: uid, type**.
6. For the partition key string value, enter "adam".
7. For the sort key string value, enter "profile".
8. Click **Start search**. We should get one result.
9. For the partition key string value, enter "john".
10. For the sort key string value, enter "item".
11. Click **+ Add filter**.
12. Enter an attribute of "collection_id" and value of "john_comics".
13. Click **Start search**. We should get multiple results.
14. Delete the filter.
15. Change the sort key value to "activity".
16. Change the sort order to **Descending**.
17. Change the query to **[Index] date-index: uid, date**.
18. For the partition key string value, enter "john".
19. Leave the sort key string value blank.
20. Click **Start search**. There should be multiple results listed in descending order (newest to oldest).
21. Refresh the browser tab with the Collectors User Profile site. It should still look the same for now.

### Implement Queries in `collectors_primary` Lambda Function

1. Copy the entirety of the `collectors_main.py` file contents (which can be [found on GitHub](https://raw.githubusercontent.com/linuxacademy/content-dynamodb-datamodeling/master/labs/microservice/solution/collectors_main.py)).
2. Navigate to Lambda in a new browser tab.
3. Click **collectors_primary**.
4. In the *Function code* section, delete the existing code for `function.py` and paste in the `collectors_main.py` [file contents](https://raw.githubusercontent.com/linuxacademy/content-dynamodb-datamodeling/master/labs/microservice/solution/collectors_main.py).
5. Click **Save**.
6. Refresh the browser tab with the Collectors User Profile site. It will take a few seconds to load this time, but it should display a lot of new information displayed now.

### Validate API Responses

1. Right-click the Collectors User Profile site, and select to view the page source.
2. Within it, look for the `self.getAll` block.
3. Copy the full `http` listed within double quotes in the `$.getJSON` line.
4. Paste it into a new browser tab. We'll get an error.
5. Replace `"+user+"` in the URL with `adam`. This will then show us all the data the table is loading onto his page.
6. In the URL, change `request=all` to `request=profile`. This will then just show his profile information from the table.

## Additional Resources

We are stepping into the role of a data architect working for a social media startup who is creating a network for people to share their various collections. The front-end web development team has provided the following data:

**CSV:**

- [profiles.csv](https://dynamodblabs.s3.amazonaws.com/collectors/data/profiles.csv)
- [activity.csv](https://dynamodblabs.s3.amazonaws.com/collectors/data/activity.csv)
- [adam/movies.csv](https://dynamodblabs.s3.amazonaws.com/collectors/data/adam/movies.csv)
- [adam/boardgames.csv](https://dynamodblabs.s3.amazonaws.com/collectors/data/adam/boardgames.csv)
- [corey/books.csv](https://dynamodblabs.s3.amazonaws.com/collectors/data/corey/books.csv)
- [craig/instruments.csv](https://dynamodblabs.s3.amazonaws.com/collectors/data/craig/instruments.csv)
- [john/comics.csv](https://dynamodblabs.s3.amazonaws.com/collectors/data/john/comics.csv)
- [john/movies.csv](https://dynamodblabs.s3.amazonaws.com/collectors/data/john/movies.csv)

**JSON (DynamoDB Batch Write formatted):**

- [profiles.json](https://dynamodblabs.s3.amazonaws.com/collectors/data/profiles.json)
- [activity.json](https://dynamodblabs.s3.amazonaws.com/collectors/data/activity.json)
- [adam/movies.json](https://dynamodblabs.s3.amazonaws.com/collectors/data/adam/movies.json)
- [adam/boardgames.json](https://dynamodblabs.s3.amazonaws.com/collectors/data/adam/boardgames.json)
- [corey/books.json](https://dynamodblabs.s3.amazonaws.com/collectors/data/corey/books.json)
- [craig/instruments.json](https://dynamodblabs.s3.amazonaws.com/collectors/data/craig/instruments.json)
- [john/comics.json](https://dynamodblabs.s3.amazonaws.com/collectors/data/john/comics.json)
- [john/movies.json](https://dynamodblabs.s3.amazonaws.com/collectors/data/john/movies.json)

They have requested that we create a data model to structure this data, as well as a DynamoDB table utilizing the data model to house the data.

They've also provided a function to load this data into the table which must be named `collectors`, additionally a skeletal Lambda function that is pre-configured to respond to requests from the API Gateway which will need to have the appropriate queries to fullfill the following access requirements added to it, as well as any necessary data management to return the data in the format that is expected by the web front end application.

Expected data for full profile load in the web front-end application:

```
{
    "picture": "URL",
    "fullName": "John Hanna",
    "location": "Washington, USA",
    "icons": ["comics", "movies"],
    "collections": {"john_comics": {"icon": "comics", "items": 
        [
            {
                "author": "Katsuhiro Otomo",
                "collection_id": "john_comics",
                "image": "https://dynamodblabs.s3.amazonaws.com/collectors/images/john/comics/Akiravol1.jpg",
                "isbn": "1935429000",
                "order": "1",
                "pages": "352",
                "pencil": "Katsuhiro Otomo",
                "published date": "October 31 2009",
                "publisher": "Kodansha Comics",
                "series": "Akira",
                "thumb": "https://dynamodblabs.s3.amazonaws.com/collectors/images/john/comics/thumbs/Akiravol1.jpg",
                "title": "Akira Vol 1",
                "type": "item"
            },
            {}
        ]
    }},
    "recentActivity": [],
    "lastAddition": {},
    "friends": []
}
```

From the above, it should be possible to access each section of the page data independently, including `profile`, `collections`, `recent activity`, `latest addition`, and `friends`.

The code used in the solution videos for this lab can be found [here](https://github.com/linuxacademy/content-dynamodb-datamodeling/tree/master/labs/microservice/solution).

*Note: The data model presented in the solution videos is intentionally suboptimal.*

