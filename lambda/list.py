import json
import os
import boto3
import decimalencoder

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['POKEMON_STORE_TABLE_NAME'])

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response

