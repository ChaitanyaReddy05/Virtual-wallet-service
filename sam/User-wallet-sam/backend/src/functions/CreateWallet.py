import json
from pyqldb.driver.qldb_driver import QldbDriver
from pyqldb.config.retry_config import RetryConfig


def lambda_handler(event, context):

    """
     This Function is used create wallet in the Wallet table.

     """

    # Parse out query string params
    CreateWalletID = event['queryStringParameters']['CreateWalletID']
    phonenum = event['queryStringParameters']['phonenum']
    panid = event['queryStringParameters']['panid']
    txn_date = event['queryStringParameters']['txn_date']
    print('CreateWalletID=' + CreateWalletID)

    # Initialize the driver
    retry_config = RetryConfig(retry_limit=3)
    print('Initializing the driver')
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)
    transactionResponse = {}
    def read_documents(transaction_executor):
        print('Querying the table', CreateWalletID)
        cursor = transaction_executor.execute_statement('SELECT * FROM Wallet WHERE walletid = ?', int(CreateWalletID))

        print(f"cursor rec {cursor}")
        first_record = next(cursor, None)
        print(f"first rec {first_record}")
        return first_record
    first_record = qldb_driver.execute_lambda(lambda executor: read_documents(executor))
    if first_record:
        transactionResponse['CreateWalletID'] = CreateWalletID
        transactionResponse['message'] = 'Wallet already exists'
    else:
        doc_1 = {'walletid': int(CreateWalletID), 'phonenum': phonenum, 'panid': panid, 'Balance': 0,
                 'last_txn_source': 'NA', 'last_txn_ref': 'NA', 'last_txn_type': 'initial wallet created',
                 'last_txn_amount': '0', 'last_txn_date': txn_date}
        def insert_documents(transaction_executor, arg_1):
            print("Inserting a document")
            transaction_executor.execute_statement("INSERT INTO Wallet ?", arg_1)
        qldb_driver.execute_lambda(lambda x: insert_documents(x, doc_1))
        # Construct the body of the response object
        transactionResponse['CreateWalletID'] = CreateWalletID
        transactionResponse['message'] = 'New wallet created successfully'

    # Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    # Return the response object
    return responseObject