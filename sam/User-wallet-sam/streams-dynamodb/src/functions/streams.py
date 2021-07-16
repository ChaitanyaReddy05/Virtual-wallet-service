import json
import amazon.ion.simpleion as ion
import base64
from aws_kinesis_agg.deaggregator import deaggregate_records
import boto3

def lambda_handler(event, context):
    raw_kinesis_records = event['Records']

    # Deaggregate all records in one call
    records = deaggregate_records(raw_kinesis_records)
    for record in records:

        # Kinesis data in Python Lambdas is base64 encoded
        payload = base64.b64decode(record['kinesis']['data'])
        # payload is the actual ion binary record published by QLDB to the stream
        ion_record = ion.loads(payload)
        print("Ion reocord: ", (ion.dumps(ion_record, binary=False)))

        if (("recordType" in ion_record) and (ion_record["recordType"] == "REVISION_DETAILS")):
            revision_data, revision_metadata = get_data_metdata_from_revision_record(ion_record)
            print(revision_metadata["version"])
            table_info = get_table_info_from_revision_record(ion_record)
            if (revision_metadata["version"] == 0):  # a new wallet created
                if (table_info and table_info["tableName"] == "Wallet" and wallet_data_has_required_fields(
                        revision_data)):
                    # add dynamo DB insertion
                    print("Proceed to create wallet in dynamo userwallet table")

                    dynamodb = boto3.resource('dynamodb')
                    table = dynamodb.Table('Wallet')
                    response = table.put_item(
                       Item={
                            'walletid': revision_data["walletid"],
                            'Balance': revision_data["Balance"],
                            'last_txn_source': revision_data["last_txn_source"],
                            'last_txn_ref': revision_data["last_txn_ref"],
                            'last_txn_type': revision_data["last_txn_type"],
                            'last_txn_amount': revision_data["last_txn_amount"],
                            'last_txn_date': revision_data["last_txn_date"],
                            'version' :  0
                        }
                    )



            else: # Balance updates
                if (table_info and table_info["tableName"] == "Wallet" and wallet_data_has_required_fields(
                        revision_data)):
                    # add dynamo db logic to update the balance
                    print("Dyanmo update balance")
                    dynamodb = boto3.resource('dynamodb')
                    table = dynamodb.Table('Wallet')
                    response = table.update_item(
                    Key={
                        'walletid': revision_data["walletid"]
                        },
                    UpdateExpression="set Balance=:a , last_txn_source=:b , last_txn_ref=:c, last_txn_type=:d ,last_txn_amount=:e ,last_txn_date=:f ,version=:g",
                    ExpressionAttributeValues={
                        ':a': revision_data["Balance"],
                        ':b': revision_data["last_txn_source"],
                        ':c': revision_data["last_txn_ref"],
                        ':d': revision_data["last_txn_type"],
                        ':e': revision_data["last_txn_amount"],
                        ':f': revision_data["last_txn_date"] ,
                        ':g': revision_metadata["version"],
                        },
                    ConditionExpression="version < :g",
                    ReturnValues="UPDATED_NEW"
                    )

            # update all transactions to dynamodb except for getfunds
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Transactions')
            response = table.put_item(
               Item={
                    'walletid': revision_data["walletid"],
                    'updated_balance': revision_data["Balance"],
                    'txn_source': revision_data["last_txn_source"],
                    'txn_ref': revision_data["last_txn_ref"],
                    'txn_type': revision_data["last_txn_type"],
                    'txn_amount': revision_data["last_txn_amount"],
                    'txn_date': revision_data["last_txn_date"],
                    'version' :  revision_metadata["version"]
                }
            )



    return {
        'statusCode': 200
    }





def get_data_metdata_from_revision_record(revision_record):
    """
    Retrieves the data block from revision Revision Record
    Parameters:
       topic_arn (string): The topic you want to publish to.
       message (string): The message you want to send.
    """

    revision_data = None
    revision_metadata = None

    if ("payload" in revision_record) and ("revision" in revision_record["payload"]):
        if ("data" in revision_record["payload"]["revision"]):
            revision_data = revision_record["payload"]["revision"]["data"]
        if ("metadata" in revision_record["payload"]["revision"]):
            revision_metadata = revision_record["payload"]["revision"]["metadata"]

    return [revision_data, revision_metadata]

def get_table_info_from_revision_record(revision_record):
    if (("payload" in revision_record) and "tableInfo" in revision_record["payload"]):
        return revision_record["payload"]["tableInfo"]


def wallet_data_has_required_fields(revision_data):
    return (("walletid" in revision_data) and ("Balance" in revision_data) and ("last_txn_source" in revision_data) and ("last_txn_ref" in revision_data) and ("last_txn_type" in revision_data)and ("last_txn_amount" in revision_data) and ("last_txn_date" in revision_data))



