import json
import time
import logging
import os

import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['POKEMON_STORE_TABLE_NAME'])

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    data = json.loads(event['body'])
    if 'pokemon' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create pokemon.")

    timestamp = int(time.time() * 1000)

    # update the todo in the database
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#pokemon_name': 'name',
        },
        ExpressionAttributeValues={
          ':name': data['pokemon'],
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #pokemon_name = :name, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
