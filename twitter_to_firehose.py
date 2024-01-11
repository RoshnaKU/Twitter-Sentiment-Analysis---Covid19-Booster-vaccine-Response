import snscrape.modules.twitter as sntwitter
import pandas as pd
import boto3
import json

ACCESS_KEY = '' #AWS Access key
SECRET_KEY = '' #AWS Secret key

query="covid booster vaccine lang:en" #twitter search keyword
tweets=[]
limit=1000 #number of tweets to be fetched
delivery_stream = '' #amazon kinesis firehouse- delivery stream name

client = boto3.client('firehose', 
                      region_name='', #aws region where firehouse delivery stream was created. eg:us-east-1
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY
                      )

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
    if len(tweets)==limit:
        break
    else:
        tweets.append([tweet.id,
            tweet.user.username,
            tweet.user.location,
            str(tweet.date),
            str(tweet.rawContent.replace('\n',' ').replace('\r',' ')),
            tweet.viewCount,
            tweet.retweetCount,
            tweet.replyCount,
            tweet.user.followersCount])
        
df= pd.DataFrame(tweets,columns=['TWEET_ID','USERNAME','USER_LOCATION','DATE','TEXT','VIEWCOUNT','RETWEETCOUNT','REPLYCOUNT','FOLLOWERSCOUNT'])

str_json_data=df.to_json(orient = 'records')
#print(str_json_data)

#put record to S3 using amazon kinesis delivery system
client.put_record(
            DeliveryStreamName=delivery_stream,
            Record={
            'Data': str_json_data
            }
        )






