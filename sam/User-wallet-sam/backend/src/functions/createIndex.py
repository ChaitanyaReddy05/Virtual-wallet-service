import json
from pyqldb.driver.qldb_driver import QldbDriver
import os
from pyqldb.config.retry_config import RetryConfig
import cfnresponse

def lambda_handler(event,context):
    """
     This Function is used add index to wallet table.

     """

    # Capture query parameters received from API
    table_name = os.environ['TABLE_NAME']
    index_attribute = os.environ['INDEX_NAME_1']

    #Initialize the driver
    retry_config = RetryConfig(retry_limit=3)
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)

    # create Index on qldb table
    statement = 'CREATE INDEX on {} ({})'.format(table_name, index_attribute)
    qldb_driver.execute_lambda(lambda executor: executor.execute_statement(statement))
    # Construct  message body
    transactionResponse = {}
    transactionResponse['Index_name'] = index_attribute
    transactionResponse['message'] = 'Index created successfully'

    # Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)
    responseData = responseObject

    #send response back to Cloudformation
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)

