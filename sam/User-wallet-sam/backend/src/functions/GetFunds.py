import json
import boto3
from pyqldb.driver.qldb_driver import QldbDriver
from pyqldb.config.retry_config import RetryConfig


def lambda_handler(event, context):
    """
       This Function is used to get funds from the Wallet table.

       """
    # Parse out query string params
    transactionResponse = {}
    WalletID = event['queryStringParameters']['WalletID']
    transactionResponse['WalletID'] = WalletID
    transactionResponse['message'] = 'Hello from Lambda land'


    # Initialize the driver

    print ('Initializing the driver')
    retry_config = RetryConfig(retry_limit=3)
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)

    def read_documents(transaction_executor):
        print ('Querying the table',WalletID)
        cursor = transaction_executor.execute_statement('SELECT * FROM Wallet WHERE walletid = ?',int(WalletID))
        for doc in cursor:
           print (doc['Balance'])
           transactionResponse['Balance'] = doc['Balance']

    qldb_driver.execute_lambda(lambda executor:read_documents(executor))

    #  Construct http response object
    print(transactionResponse)
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    # Return the response object

    return responseObject
