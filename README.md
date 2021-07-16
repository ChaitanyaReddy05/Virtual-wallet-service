# Virtual-wallet-service

https://app.diagrams.net/#HChaitanyaReddy05%2FVirtual-wallet-service%2Fmaster%2FUntitled%20Diagram.drawio

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
