# Twitter Sentiment Analysis – Covid19 Booster vaccine Response

## Overview
As part of my learning journey, I wanted to do a case study that involves real world, big data analytics problems with cloud solutions. That is when I came across one of the whitepapers published by amazon https://docs.aws.amazon.com/pdfs/whitepapers/latest/big-data-analytics-options/big-data-analytics-options.pdf#example-3-sentiment-analysis-of-social-media 
With this whitepaper as base and of course with some tweaks to the sample system design (due to my budget constraints), I decided to analyze and find sentiment expressed by the Twitter users in their tweets related to covid19 booster vaccine. 
The global impact of the COVID-19 pandemic has been unprecedented, but so too have the speed of development and efficacy of vaccines for COVID-19. When it comes to getting a vaccine to protect yourself against a disease like COVID-19, booster shots can be a normal part of the vaccination process. Some individuals welcome the booster vaccine doses as a way to increase protection against the virus, while others are more hesitant or skeptical. Supporters of booster shots point to the benefits of increased immunity and protection against new variants of the virus, as well as the potential to reduce the severity of illness and hospitalization. However, critics argue that booster shots may not be necessary for everyone, and that resources should instead be focused on increasing vaccine access for those who have not yet received their first doses.
This case study will go through a data ingestion pipeline, capture covid19 booster vaccine tweets data, ingest in AWS, process, give sentiment scores to each tweet, and later visualize it on a dashboard.

System design or architecture of this case study is as follows:

![Tweet_sentiment_architecture_v2](https://user-images.githubusercontent.com/125311073/236038749-bf9b3c6e-cad6-4108-a9b2-eec727156d06.jpg)
 
## Services used
1.	**Amazon EC2**: Amazon EC2 is used for scalable computing capacity in the AWS Cloud so you can develop and deploy applications without hardware constraints.
2.	**Amazon Kinesis Data Firehose**: an extract, transform, and load (ETL) service that reliably captures, transforms, and delivers streaming data to data lakes
3.	**Amazon S3**: Amazon S3 is an object storage service that provides manufacturing scalability, data availability, security, and performance.
4.	**AWS IAM**: Identity and access management manage access to AWS services and resources securely.
5.	**AWS Lambda**: Lambda is a computing service that allows programmers to run code without creating or managing servers.
6.	**Amazon Comprehend**: a natural-language processing (NLP) service that uses machine learning to uncover valuable insights and connections in text.
7.	**Amazon DynamoDB**: a fully managed, serverless, key-value NoSQL database designed to run high-performance applications at any scale.
8.	**Amazon Kinesis Data Streams**: a fully managed, serverless data streaming service that stores and ingests various streaming data in real time at any scale.
9.	**Snowflake Data Cloud**: Snowflake's Data Cloud is powered by an advanced data platform provided as a self-managed service. Snowflake enables data storage, processing, and analytic solutions that are faster, easier to use, and far more flexible than traditional offerings.

## Dataset Used
For this case study, a scraper called ‘snscrape’ was used to fetch twitter data. 
‘snscrape’ is a scraper for social networking services (SNS). It scrapes things like user profiles, hashtags, or searches and returns the discovered items, e.g., the relevant posts.
Requirement for snscrape: snscrape requires Python 3.8 or higher. The Python package dependencies are installed automatically when you install snscrape.

## Project Stages
### 1.	Tweet Processing and Upload
#### Amazon EC2 instance:
  A Linux machine was used to fulfil the case study’s purpose. This EC2 machine serves 2 purposes:
  1. Tweets were collected using a python script ‘twitter_to_firehose.py’ placed on this EC2 machine  
  *twitter_to_firehose.py*: This script fetches tweets convert to JSON, put them in the firehose delivery system which in turn ingests the twitter data in JSON format to an S3 bucket.
  Note: For this case study, I have fetched only tweets written in English. If search data was irrespective of language, then we have to translate them to English using Amazon translate.

  ##### Prerequisite for this script to run:
  1. AWS user access key and secret key to access AWS services
  2. Create an S3 bucket to which the fetched tweets will be loaded in JSON format. 
  3. Create a delivery stream in Amazon Kinesis Data Firehose with source as ‘Direct Put’ and Target as S3 bucket created in Step 2.
  4. Install Python and necessary packages on EC2 machine as and when needed
  
  2.	Schedule twitter data fetch using crontab to run daily every 15 mins
  Create a .cron file(crontab_to_fetch_twitter_data.cron) to schedule the script to stream data every 15 minutes

### 2.	Fetching raw data and performing sentiment analysis
Whenever data is streamed from twitter, S3 bucket will invoke a Lambda function to analyse the raw tweets using Amazon Comprehend to use natural language-processing (NLP) to perform sentiment analysis.
Therefore, the trigger of this lambda function has to be configured to point to the S3 bucket, so that whenever there is a new stream of data, the lambda function is triggered. 
Sentiment data together with the raw tweet data is then loaded into a table created in Amazon Dynamo DB which is going to act as a real-time streaming Database.
  #### Prerequisites to run the Lambda function:
  1.	A table has to be created in DynamoDB to load the incoming data

### 3.	Data Warehousing
To generate reports/dashboard on the sentiment data loaded into Dynamo DB, it has to be warehoused. I initially had a thought to use Glue crawlers and crawl the data to AWS Athena which in turn can be visualized in Amazon Quicksight(as per the whitepaper example). However, I decided to go with Snowflake for both warehousing and data visualization because   Glue Crawlers and Athena data scan could cost me due to growing data whereas in case of snowflake, I was still on my free trial period.  




