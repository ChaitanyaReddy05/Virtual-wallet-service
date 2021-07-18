# Virtual-wallet-service

In the gaming industry, users are often allowed to open accounts and make monetary transactions; they can exchange real money for in-game currency. Players want to be able to add or withdraw funds quickly, and they also want to know how their balance has changed over time. Having this information available helps our customers better understand their users’ behavior so they can identify marketing opportunities and improve sales predictions.

The demo virtual wallet service was built as part of hackathon conducted by tech giant. This service can be used by gaming companies to manage players account balances including virtual currencies.

# Architechture

![Architechture](https://github.com/ChaitanyaReddy05/Virtual-wallet-service/blob/master/architechture.png)


# Solution Components

API Gateway :  API Gateway acts a entrypoint to the whole stack exposing the required API's - createwallet, addfunds, getfunds,withdrawfunds and transactions. API Gateway is a fully managed service that makes it relatively easy for developers to create, publish, maintain, monitor, and secure APIs at any scale.  

Lambda : Lambda is a serverless compute service that lets you run code without provisioning or managing servers.      Lambda is used as a driving force which handles the entire backend logic and stitching the required components.  

Amazon QLDB : QLDB is a fully managed ledger database that provides a transparent, immutable, and cryptographically verifiable transaction log owned by a central trusted authority. It is a purpose built ledger database having the features like -history of all modifications, optimistic concurrency control and serializable isolation to ensure that no one can modify account balances while updates are performed, preventing possible race conditions

Amazon QLDB - Amazon Kinesis Data Streams : This is used to support use cases such as analytics and downstream event processing, or tasks better supported by other purpose built database, whilst retaining QLDB as the source of truth. QLDB Streams is a feature that allows changes made to the journal to be continuously written in near real time to a destination Kinesis Data Stream. Consumers which is a lambda  can subscribe to the stream, and take appropriate action - to share these event of data records to DyanamoDB. 

DynamoDB : DynamoDB is a key-value and document database that delivers single-digit millisecond performance at any scale. It’s a fully managed, multi-Region, multi-active, and durable database with built-in security, backup and restore, and in-memory caching for internet-scale applications. Using these services, we make transaction history available via an API - transactions


# Deployment Steps :

Please navigate to the respective individual folders as per the sequence mentioned below for the deployment :

1) sam/User-wallet-sam/backend
2) sam/User-wallet-sam/streams-dynamodb
3) Front-end deployment 


Front-end Deployment :
For deploying the Front end applicationn which is a game site , we need below pre-requisties:
1) [pip](https://pip.pypa.io/en/stable/cli/pip_install/)
2) python 3.7
3) App specific requirements.

For deploying the application specific requirements:
```bash
pip install -r requirements.txt
```

Once app specific requirements are installed :
run:
```bash
python manage.py migrate
```

To start the application :
```bash
python manage.py runserver
```
