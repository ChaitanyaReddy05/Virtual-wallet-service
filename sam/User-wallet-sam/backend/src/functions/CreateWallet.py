import json
from pyqldb.driver.qldb_driver import QldbDriver
from pyqldb.config.retry_config import RetryConfig


def lambda_handler(event, context):
    # 1. Parse out query string params
    CreateWalletID = event['queryStringParameters']['CreateWalletID']
    phonenum = event['queryStringParameters']['phonenum']
    panid = event['queryStringParameters']['panid']
    txn_date = event['queryStringParameters']['txn_date']
    print('CreateWalletID=' + CreateWalletID)
    retry_config = RetryConfig(retry_limit=3)
    # Initialize the driver
    print('Initializing the driver')
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)
    doc_1 = {'walletid': int(CreateWalletID), 'phonenum': phonenum, 'panid': panid, 'Balance': 0,
             'last_txn_source': 'NA', 'last_txn_ref': 'NA', 'last_txn_type': 'initial wallet created',
             'last_txn_amount': '0', 'last_txn_date': txn_date}

    def insert_documents(transaction_executor, arg_1):
        print("Inserting a document")
        transaction_executor.execute_statement("INSERT INTO Wallet ?", arg_1)

    qldb_driver.execute_lambda(lambda x: insert_documents(x, doc_1))
    # 2. Construct the body of the response object
    transactionResponse = {}
    transactionResponse['CreateWalletID'] = CreateWalletID
    transactionResponse['message'] = 'New wallet created successfully'

    # 3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    # 4. Return the response object
    return responseObject