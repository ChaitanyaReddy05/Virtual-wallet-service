import time

import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import boto3
from .forms import UserRegisterForm,RedeemPointsForm
from .models import wallet
from django.contrib.auth.models import User
from datetime import datetime
from boto3.dynamodb.conditions import Key
from secrets import choice
import string


# Create your views here.

@login_required
def home(request,pk):
    dynamodb = boto3.resource('dynamodb')
    table_wallet = dynamodb.Table('userwallet')
    wallet_response = table_wallet.query(
        KeyConditionExpression=Key('walletid').eq(pk),
        ScanIndexForward=False,
    )
    if wallet_response['Items']:

        url = f'https://ghfh9pbqnf.execute-api.us-east-1.amazonaws.com/Develop/funds?WalletID={pk}'
        r = requests.get(url, headers={'authorizationToken': 'abc123'})
        balance_details = r.json()

        table = dynamodb.Table('transactions')
        response = table.query(
            KeyConditionExpression=Key('walletid').eq(pk),
            ScanIndexForward = False,
            Limit = 5
        )
        context = {
            'Balance' : balance_details['Balance'],
            'txn_list' : response["Items"],
            'walletid' : pk,
            'wallet' : True

        }
    else:
        context = {
            'wallet': False,
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
            #url = f'https://ghfh9pbqnf.execute-api.us-east-1.amazonaws.com/Develop/createwallet?CreateWalletID={wallet_id}&txn_date={datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            #r = requests.post(url,headers={ 'authorizationToken': 'abc123' })

            #if r.status_code == 200:
                #data = r.json()
                #print("Wallet created successfully")

            messages.success(request,f'Account created sucessfully for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'userwallet/register.html',{'form': form})

@login_required
def login_redirect(request):
    user_logged = User.objects.filter(username=request.user.username).first()
    print(user_logged.wallet.walletid)
    return redirect('game_home', pk=wallet.objects.filter(user=user_logged).first().walletid)

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

@login_required
def game_home(request,pk):
    return render(request,'userwallet/game_home.html',{'pk':pk,'gamepoints':wallet.objects.get(pk=pk).gamepoints})

@login_required
def create_wallet_request(request,pk):
    return render(request, 'userwallet/create_wallet_request.html', {'walletid': pk})



@login_required
def create_wallet_post(request,pk):
    if request.method == 'POST':
            phonenum = request.POST["phonenum"]
            panid = request.POST["panid"]
            url = f'https://ghfh9pbqnf.execute-api.us-east-1.amazonaws.com/Develop/createwallet?CreateWalletID={pk}&phonenum={phonenum}&panid={panid}&txn_date={datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            r = requests.post(url,headers={ 'authorizationToken': 'abc123' })

            if r.status_code == 200:
                data = r.json()
                print("Wallet created successfully")
            time.sleep(5)

    return redirect('home',pk=pk)

@login_required
def redeempoints(request,pk):
    txn_ref = ''.join([choice(string.ascii_uppercase + string.digits) for _ in range(9)])

    if request.method == 'POST':
        form = RedeemPointsForm(request.POST)
        dynamodb = boto3.resource('dynamodb')
        table_wallet = dynamodb.Table('userwallet')
        wallet_response = table_wallet.query(
            KeyConditionExpression=Key('walletid').eq(pk),
            ScanIndexForward=False,
        )
        if wallet_response['Items']:

            if form.is_valid():
                url = f'https://ghfh9pbqnf.execute-api.us-east-1.amazonaws.com/Develop/funds?WalletID={pk}'
                r = requests.get(url, headers={'authorizationToken': 'abc123'})


                balance_details = r.json()

                gamepoints = form.cleaned_data.get('gamepoints')

                Balance = balance_details['Balance']
                if int(gamepoints) <= Balance:
                    user_wallet = User.objects.get(pk=request.user.id).wallet
                    user_wallet.gamepoints += gamepoints
                    user_wallet.save()
                    url = f'https://ghfh9pbqnf.execute-api.us-east-1.amazonaws.com/Develop/deletefunds?WalletID={pk}&txn_source=CAPG-Game&txn_ref={txn_ref}&txn_type=DEBIT&txn_amount={gamepoints}&txn_date={datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                    r = requests.post(url, headers={'authorizationToken': 'abc123'})

                    if r.status_code == 200:
                        data = r.json()
                    time.sleep(5)
                    messages.success(request, f'Balance of ₹ {gamepoints} debited from wallet  successfully ')
                    return redirect('home',pk=pk)
                else:
                    messages.info(request, f'Insufficient Balance ')
                    form = RedeemPointsForm()
        else:
            messages.info(request, f'Please create a wallet to add points ')
            form = RedeemPointsForm()





    else:
        form = RedeemPointsForm()
    return render(request,'userwallet/redeempoints.html',{'form': form,'pk':pk,'gamepoints':wallet.objects.get(pk=pk).gamepoints})






