import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['POKEMON_STORE_TABLE_NAME'])

def handler(event, context):
    # delete the todo from the database
    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200
    }

    return response
