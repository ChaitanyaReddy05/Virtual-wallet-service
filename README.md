# Virtual-wallet-service

In the gaming industry, users are often allowed to open accounts and make monetary transactions; they can exchange real money for in-game currency. Players want to be able to add or withdraw funds quickly, and they also want to know how their balance has changed over time. Having this information available helps our customers better understand their users’ behavior so they can identify marketing opportunities and improve sales predictions.

The demo virtual wallet service was built as part of hackathon conducted by tech giant. This service can be used by gaming companies to manage players account balances including virtual currencies.

# Architechture

![Architechture](https://github.com/ChaitanyaReddy05/Virtual-wallet-service/blob/master/architechture.png)

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
