import json
import boto3 # type: ignore

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Connections')

def lambda_handler(event, context):
    apigateway = boto3.client(
        'apigatewaymanagementapi',
        endpoint_url="https://desd07jxq2.execute-api.ap-south-1.amazonaws.com/production"
    )

    body = json.loads(event['body'])
    message = body.get('message')

    connections = table.scan()['Items']

    for connection in connections:
        try:
            apigateway.post_to_connection(
                ConnectionId=connection['connectionId'],
                Data=json.dumps({'message': message})
            )
        except:
            pass

    return {'statusCode': 200}
