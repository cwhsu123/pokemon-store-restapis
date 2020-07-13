import json
import os
import boto3
import time
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['POKEMON_STORE_TABLE_NAME'])

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    data = json.loads(event['body'])
    if 'pokemon' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create pokemon.")

    timestamp = str(time.time())

    item = {
            'id': str(uuid.uuid1()),
            'name': data['pokemon'],
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }   
    
    # write the pokemon to the table
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
