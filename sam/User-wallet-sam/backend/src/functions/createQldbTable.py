import json
from pyqldb.driver.qldb_driver import QldbDriver
import os
from pyqldb.config.retry_config import RetryConfig
import cfnresponse
def lambda_handler(event,context):
    retry_config = RetryConfig(retry_limit=3)
    table_name = os.environ['WALLET_TABLE_NAME']
    statement = 'CREATE TABLE {}'.format(table_name)
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)

    statement = 'CREATE TABLE {}'.format(table_name)
    qldb_driver.execute_lambda(lambda executor: executor.execute_statement(statement))
    transactionResponse = {}
    transactionResponse['CreateWalletID'] = table_name
    transactionResponse['message'] = 'Table created successfully'

    # 3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)
    responseData = responseObject
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)

