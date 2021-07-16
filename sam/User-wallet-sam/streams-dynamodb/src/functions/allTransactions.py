import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal


def lambda_handler(event, context):

    """
    This Function is used to retrieve the history of transactions from dynamodb
    based on the walletid as partition key.

    """
    # Parse out query parameters
    WalletID = event['queryStringParameters']['WalletID']

    #initialize dynamodb client
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

    #  Return the response object

    return responseObject

