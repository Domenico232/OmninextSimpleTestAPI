import json
import boto3
import logging
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    user_id = body['id']
    user_name = body['name']

    table.put_item(
        Item={
            'id': user_id,
            'name': user_name
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('User created successfully!')
    }



import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
        
def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters') or event.get('QueryStringParameters')
        if query_params:
            user_id = query_params.get('id')
            if user_id:
                logger.info("Received user_id: %s", user_id)
                
                response = table.get_item(
                    Key={
                        'id': user_id
                    }
                )

                item = response.get('Item')
                if not item:
                    return {
                        'statusCode': 404,
                        'body': json.dumps('User not found')
                    }

                return {
                    'statusCode': 200,
                    'body': json.dumps(item, default=decimal_default)
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps('Missing user id')
                }
    except Exception as e:
        logger.error("Error processing request: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
