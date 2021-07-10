import time

import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import boto3
from .forms import UserRegisterForm
from .models import wallet
from django.contrib.auth.models import User
from datetime import datetime
from boto3.dynamodb.conditions import Key
from secrets import choice
import string


# Create your views here.

@login_required
def home(request,pk):
    url = f'https://ghfh9pbqnf.execute-api.us-east-1.amazonaws.com/Develop/funds?WalletID={pk}'
    r = requests.get(url, headers={'authorizationToken': 'abc123'})
    balance_details = r.json()

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('transactions')
    response = table.query(
        KeyConditionExpression=Key('walletid').eq(pk),
        ScanIndexForward = False,
        Limit = 5
    )
    context = {
        'Balance' : balance_details['Balance'],
        'txn_list' : response["Items"],
        'walletid' : pk

    }

    return render(request,'userwallet/home.html',context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_wallet = wallet(user=User.objects.filter(username=username).first())
            user_wallet.save()
            user_logged = User.objects.filter(username=username).first()
            wallet_id = wallet.objects.filter(user=user_logged).first().walletid

            # INVOKE CREATE WALLET API HERE
            url = f'https://ghfh9pbqnf.execute-api.us-east-1.amazonaws.com/Develop/createwallet?CreateWalletID={wallet_id}&txn_date={datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            r = requests.post(url,headers={ 'authorizationToken': 'abc123' })

            if r.status_code == 200:
                data = r.json()
                print("Wallet created successfully")

            messages.success(request,f'Account created sucessfully for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'userwallet/register.html',{'form': form})

@login_required
def login_redirect(request):
    user_logged = User.objects.filter(username=request.user.username).first()
    return redirect('home', pk=wallet.objects.filter(user=user_logged).first().walletid)

def addfunds(request,pk):
    if request.method == 'POST':
        phonenum = request.POST["phonenum"]
        amount   = request.POST["amount"]
        payment_gw = request.POST["payment_gw"]
    context = {
        'walletid' : pk,
        'phonenum' : phonenum,
        'amount'   : amount,
        'payment_gw' : payment_gw
    }
    return render(request,'userwallet/txn_confirmation.html',context)



def postfunds(request,pk):
    if request.method == 'POST':
            txn_amount = request.POST["amount"]
            payment_gw = request.POST["payment_gw"]

            txn_ref = ''.join([choice(string.ascii_uppercase + string.digits) for _ in range(9)])
            # INVOKE addfunds  API HERE
            url = f'https://ghfh9pbqnf.execute-api.us-east-1.amazonaws.com/Develop/addfunds?WalletID={pk}&txn_source={payment_gw}&txn_ref={txn_ref}&txn_type=CREDIT&txn_amount={txn_amount}&txn_date={datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            r = requests.post(url,headers={ 'authorizationToken': 'abc123' })

            if r.status_code == 200:
                data = r.json()
            messages.success(request,f'Balance of ₹ {txn_amount} added to wallet  sucessfully ')
            time.sleep(5)
            return redirect('home',pk=pk)

def all_transactions(request,pk):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('transactions')
    response = table.query(
        KeyConditionExpression=Key('walletid').eq(pk),
        ScanIndexForward = False,
    )
    context = {
        'txn_list' : response["Items"],
        'walletid' : pk

    }

    return render(request,'userwallet/all_transactions.html',context)







