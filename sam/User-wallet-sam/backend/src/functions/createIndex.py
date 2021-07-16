import json
from pyqldb.driver.qldb_driver import QldbDriver
import os
from pyqldb.config.retry_config import RetryConfig
import cfnresponse

def lambda_handler(event,context):
    retry_config = RetryConfig(retry_limit=3)
    table_name = os.environ['TABLE_NAME']
    index_attribute = os.environ['INDEX_NAME_1']
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)
    statement = 'CREATE INDEX on {} ({})'.format(table_name, index_attribute)
    qldb_driver.execute_lambda(lambda executor: executor.execute_statement(statement))
    transactionResponse = {}
    transactionResponse['Index_name'] = index_attribute
    transactionResponse['message'] = 'Index created successfully'

    # 3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)
    responseData = responseObject
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)

