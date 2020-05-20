import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')
table_name = 'posts'


def create(event, context):
    logger.info(f'Incoming request is: {event}')

    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while creating post."
    }

    post = event['body']
    res = dynamodb.put_item(
        TableName=table_name, Item=dict_to_item(json.loads(post)))

    # If creation is successful
    if res['ResponseMetadata']['HTTPStatusCode'] == 200:
        response = {
            "statusCode": 201,
            "body": post
        }

    return response


def get(event, context):
    logger.info(f'Incoming request is: {event}')
    # Set the default error response
    response = {
        "statusCode": 500,
        "body": "An error occured while creating post."
    }

    post_id = event['pathParameters']['postId']

    post_query = dynamodb.get_item(
        TableName=table_name, Key={'id': {'N': post_id}})

    if 'Item' in post_query:
        post = post_query['Item']
        logger.info(f'Post is: {post}')
        response = {
            "statusCode": 200,
            "body": json.dumps(item_to_dict(post))
        }

    return response


def all(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def update(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def delete(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

# A utility function for DynamoDB to convert a dict into DynamoDB object


def dict_to_item(raw):
    if type(raw) is dict:
        resp = {}
        for k, v in raw.items():
            if type(v) is str:
                resp[k] = {
                    'S': v
                }
            elif type(v) is int:
                resp[k] = {
                    'N': str(v)
                }
            elif type(v) is dict:
                resp[k] = {
                    'M': dict_to_item(v)
                }
            elif type(v) is bool:
                resp[k] = {
                    'BOOL': v
                }
            elif type(v) is list:
                resp[k] = []
                for i in v:
                    resp[k].append(dict_to_item(i))

        return resp
    elif type(raw) is str:
        return {
            'S': raw
        }
    elif type(raw) is int:
        return {
            'I': str(raw)
        }


def item_to_dict(raw):
    if type(raw) is dict:
        resp = {}
        for k, v in raw.items():
            if 'S' in v:
                resp[k] = v['S']
            elif 'N' in v:
                resp[k] = int(v['N'])
            elif 'M' in v:
                resp[k] = item_to_dict(v['M'])
            elif 'BOOL' in v:
                resp[k] = bool(v['BOOL'])
            elif v is list:
                resp[k] = []
                for i in v:
                    resp[k].append(dict_to_item(i))
    return resp
