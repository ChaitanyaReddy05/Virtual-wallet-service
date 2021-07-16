import json
from pyqldb.driver.qldb_driver import QldbDriver
import os
from pyqldb.config.retry_config import RetryConfig
import cfnresponse

def lambda_handler(event,context):

    """
     This Function is used create wallet table in qldb.

     """

    # Capture query parameters received from API
    table_name = os.environ['WALLET_TABLE_NAME']
    statement = 'CREATE TABLE {}'.format(table_name)
    # Initialize the driver
    retry_config = RetryConfig(retry_limit=3)
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)

    # create table
    statement = 'CREATE TABLE {}'.format(table_name)
    qldb_driver.execute_lambda(lambda executor: executor.execute_statement(statement))

    # Construct body
    transactionResponse = {}
    transactionResponse['CreateWalletID'] = table_name
    transactionResponse['message'] = 'Table created successfully'

    # Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)
    responseData = responseObject

    #send response back to Cloudformation
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)

