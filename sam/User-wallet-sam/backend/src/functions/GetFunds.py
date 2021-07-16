import json
import boto3
from pyqldb.driver.qldb_driver import QldbDriver
from pyqldb.config.retry_config import RetryConfig


def lambda_handler(event, context):
    WalletID = event['queryStringParameters']['WalletID']
    transactionResponse = {}
    transactionResponse['WalletID'] = WalletID
    transactionResponse['message'] = 'Hello from Lambda land'
    retry_config = RetryConfig(retry_limit=3)

    # Initialize the driver

    print ('Initializing the driver')
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)

    def read_documents(transaction_executor):
        print ('Querying the table',WalletID)
        cursor = transaction_executor.execute_statement('SELECT * FROM Wallet WHERE walletid = ?',int(WalletID))
        for doc in cursor:
           print (doc['Balance'])
           transactionResponse['Balance'] = doc['Balance']

    qldb_driver.execute_lambda(lambda executor:read_documents(executor))

    # 3. Construct http response object
    print(transactionResponse)
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    # 4. Return the response object

    return responseObject
