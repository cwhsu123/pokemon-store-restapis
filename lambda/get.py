import os
import json
import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['POKEMON_STORE_TABLE_NAME'])

def handler(event, context):

    # fetch pokemon from dynamo
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
