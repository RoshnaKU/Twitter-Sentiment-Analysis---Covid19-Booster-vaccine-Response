import boto3
import json
import ast

s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')
table = dynamodb_client.Table('tweet_booster_vaccine_sentiment')
comprehend = boto3.client('comprehend')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    obj_name = s3_client.get_object(Bucket=bucket,Key=key)
    read_obj = obj_name['Body'].read().decode("utf-8")
    read_file = ast.literal_eval(read_obj)
    
    for row in read_file:
        table.put_item(
        Item={
            'TWEET_ID': row['TWEET_ID'],
            'USERNAME': row['USERNAME'],
            'USER_LOCATION': row['USER_LOCATION'],
            'DATE': row['DATE'],
            'TEXT': row['TEXT'],
            'VIEWCOUNT': row['VIEWCOUNT'],
            'RETWEETCOUNT': row['RETWEETCOUNT'],
            'REPLYCOUNT': row['REPLYCOUNT'],
            'FOLLOWERSCOUNT': row['FOLLOWERSCOUNT'],
            'SENTIMENT': comprehend.detect_sentiment(Text=row['TEXT'],LanguageCode='en')['Sentiment']
            }
        )   
    
    return "success"
