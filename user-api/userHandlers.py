import json
import boto3
from flask import Flask, request

#Inizializzazione dell'Applicazione Flask e Risorse DynamoDB
app = Flask(__name__)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

#Endpoint e funzione per la creazione di un nuovo utente
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    response = table.put_item(Item=data)
    return json.dumps({'message': 'User created successfully'}), 200

#Endpoint e funzione per trovare un utente nel database con id
@app.route('/user/<id>', methods=['GET'])
def get_user_by_id(id):
    response = table.get_item(Key={'id': id})
    if 'Item' in response:
        return json.dumps(response['Item']), 200
    else:
        return json.dumps({'message': 'User not found'}), 404
    

#integrazione metodi in aws lambda
""" def lambda_handler(event, context):
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
    } """

""" def decimal_default(obj):
    if isinstance(obj):
        return int(obj) if obj % 1 == 0 else float(obj)
        
def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters') or event.get('QueryStringParameters')
        if query_params:
            user_id = query_params.get('id')
            if user_id:

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
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid request: no query string parameters found')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        } """

