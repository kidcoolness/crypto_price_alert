import time
from bs4 import BeautifulSoup
import requests
import re
import email_send as e_mail

def import_config():
    coins = {}
    pur_pri = 0
    des_inc = 0
    with open('config.txt','r') as file:
        for i in file:
            if "Please" and "email:" in i:
                i = i.strip("\n").split(":")
                email = i[1]
            elif "Password" in i:
                password = i.split("'")
                password = password[1]
            elif '-' in i and "coins" not in i:
                i = i.strip('\n,-').split(', ')
                pur_pri = i[1].replace(',','')
                des_inc = i[2]
                coins[i[0]] = [pur_pri,des_inc]  
    return coins,email,password
                


    return email

def price_check(coin):
    if " " in coin:
        coin = coin.replace(" ","-")
        link = f"https://coinmarketcap.com/currencies/{coin}/"
    else:
        link = f"https://coinmarketcap.com/currencies/{coin}/"
    print(link)
    req = requests.get(link).text
    soup = BeautifulSoup(req , "html.parser")
    x = soup.find_all('div',class_ = 'priceValue')
    x = re.split('>|<', str(x))
    x = x[4][1:]
    x = x.strip(',')
    if ',' in x:
        x = x.replace(',','')
    return float(x)
    
def price_compare(i,coins,price):
    perc = float(coins[i][1])
    #vars
    print(coins[i][0],perc,price)
    #print change in price
    price_diff = price - float(coins[i][0])
    change = price_diff/float(coins[i][0])
    print(f"Current Profit % for {i}: {'{:.0%}'.format(change)}")
    print()
    if change > perc:
        sell = True
        return sell

def main():
    sell = False
    coins,email,password = import_config()
    while True:
        for i in coins:
            price = price_check(i)
            sell = price_compare(i,coins,price)
            if sell == True:
                e_mail.alert_user(i,email,password)
        time.sleep(30)
            
main()