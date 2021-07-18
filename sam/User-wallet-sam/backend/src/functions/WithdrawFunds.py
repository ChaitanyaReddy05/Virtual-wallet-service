import json
import boto3
from pyqldb.driver.qldb_driver import QldbDriver
from pyqldb.config.retry_config import RetryConfig


def lambda_handler(event, context):
    """
       This Function is used to withdraw funds from the Wallet table.

       """


    # Parse out query string params

    WalletID = event['queryStringParameters']['WalletID']
    txn_source = event['queryStringParameters']['txn_source']
    txn_ref = event['queryStringParameters']['txn_ref']
    txn_type = event['queryStringParameters']['txn_type']
    txn_amount = event['queryStringParameters']['txn_amount']
    txn_date = event['queryStringParameters']['txn_date']


    # Initialize the driver
    retry_config = RetryConfig(retry_limit=3)
    print('Initializing the driver')
    qldb_driver = QldbDriver('UserWallet', retry_config=retry_config)

    # Get old Balance
    def read_documents(transaction_executor):
        print('Querying the table', WalletID)
        cursor = transaction_executor.execute_statement('SELECT * FROM Wallet WHERE walletid = ?', int(WalletID))
        for doc in cursor:
            print(doc['Balance'])
            return doc['Balance']

    old_balance = qldb_driver.execute_lambda(lambda executor: read_documents(executor))
    transactionResponse = {}
    responseObject = {}
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    transactionResponse['WalletID'] = WalletID

    # check if Balance is greater or equal to funds to withdraw
    if int(txn_amount) > int(old_balance):
        responseObject['statusCode'] = 402
        transactionResponse['message'] = 'Insufficient funds to redeem'
    else:
        new_balance = old_balance - int(txn_amount)
        def update_documents(transaction_executor, txn_source, txn_ref, txn_type, txn_amount, new_balance, txn_date,
                             WalletID):
            transaction_executor.execute_statement(
                "UPDATE Wallet SET last_txn_source = ? , last_txn_ref = ? , last_txn_type = ? , last_txn_amount = ? ,Balance = ? ,last_txn_date = ? WHERE walletid = ?",
                txn_source, txn_ref, txn_type, int(txn_amount), new_balance, txn_date, int(WalletID))

        qldb_driver.execute_lambda(
            lambda x: update_documents(x, txn_source, txn_ref, txn_type, txn_amount, new_balance, txn_date, WalletID))
        # Construct http response object

        transactionResponse['current_balance'] = new_balance
        transactionResponse['old_balance'] = old_balance

        transactionResponse['message'] = 'Funds redeemed from the wallet'
        print(transactionResponse)

        responseObject['statusCode'] = 200

    responseObject['body'] = json.dumps(transactionResponse)

    # Return the response object

    return responseObject
