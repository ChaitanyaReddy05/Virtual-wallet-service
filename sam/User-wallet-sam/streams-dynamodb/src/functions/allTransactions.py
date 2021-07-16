import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal


def lambda_handler(event, context):
    # TODO implement
    WalletID = event['queryStringParameters']['WalletID']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Transactions')
    print(f"WalletID{WalletID}")
    response = table.query(
        KeyConditionExpression=Key('walletid').eq(int(WalletID)),
        ScanIndexForward=False,
    )

    def default(obj):
        if isinstance(obj, Decimal):
            return str(obj)
        raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(response, default=default)

    print(response)
    print(responseObject)

    # 4. Return the response object

    return responseObject

