select tweet_senti:dynamodb.NewImage.USERNAME.S::string as USERNAME,
tweet_senti:dynamodb.NewImage.USER_LOCATION.S::string as USER_LOCATION,
tweet_senti:dynamodb.NewImage.DATE.N::string as DATE,
tweet_senti:dynamodb.NewImage.RETWEETCOUNT.N::string as RETWEETCOUNT,
tweet_senti:dynamodb.NewImage.VIEWCOUNT.N::string as VIEWCOUNT,
tweet_senti:dynamodb.NewImage.TWEET_ID.N::string as TWEET_ID,
tweet_senti:dynamodb.NewImage.FOLLOWERSCOUNT.N::string as FOLLOWERSCOUNT,
tweet_senti:dynamodb.NewImage.REPLYCOUNT.N::string as REPLYCOUNT,
tweet_senti:dynamodb.NewImage.TEXT.S::string as TWEET,
tweet_senti:dynamodb.NewImage.SENTIMENT.S::string as SENTIMENT
from TWITTER.AWS_S3.TWEET_BV_SENTIMENT;