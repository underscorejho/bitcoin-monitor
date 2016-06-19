#!/usr/bin/python

# Jared Henry Oviatt


########
#
# TODO:
## DONE
## get accurate prices with Coinbase
## integrate Coinbase API
## write ledger to file on run
## use ledger to keep track of buys/sells instead of db
## read day and balance from ledger
## ... 'Day: 5, Bought $xx.xx' OR 'Day: 5, Sold $xxx.xx at xxx.xx% profit
## ... 'Day: 5, Balance: $5000, Buys: 3, BTC: .23, Investment: $105'
#######
# factor in coinbase fees
#######
# AWS:
# set cron jobs to run
# run on every 5th/10th day (two cron jobs)
# set up email notification reporting last months logs
#
########

from urllib.request import urlopen
from coinbase.wallet.client import Client
import sys
import os.path

def get_ledger():
  if not os.path.isfile('../log/ledger.ldg'):
    print("ERROR: new ledger file is needed.\nCopy new_ledger.ldg into log/ledger.ldg and update balance.\n")
    return 1
  f = open('../log/ledger.ldg', 'r')
  ledger = f.readlines()
  f.close
  
  state = ledger[-1].split(',')
  state = [x.strip() for x in state]
  
  return int(state[0][5:]), float(state[1][10:]), int(state[2][6:]), float(state[3][5:]), float(state[4][13:])

def write_ledger(ledger_list):
  # ledger_list = [day+1, balance, buys, btc, cost, action, amount]
  buy_str = 'Day: ' + str(ledger_list[0]) + ', Bought $' + str(ledger_list[6]) + '\n' 
  sell_str = 'Day: ' + str(ledger_list[0]) + ', Sold $' + str(ledger_list[6]) + 'for ' + str(ledger_list[4]/ledger_list[6]) + '% profit' + '\n'
  summary_str = 'Day: ' + str(ledger_list[0]) + ', Balance: $' + str(ledger_list[1]) + ', Buys: ' + str(ledger_list[2]) + ', BTC: ' + str(ledger_list[3]) + ', Investment: $' + str(ledger_list[4]) + '\n'

  if ledger_list[5] == 'buy':
    action_str = buy_str
  elif ledger_list[5] == 'sell':
    action_str = sell_str
  else:
    print('ERROR: wut')

  f = open('../log/ledger.ldg', 'r')
  ledger = f.readlines()
  f.close()

  ledger = ledger[:-1]
  ledger.append(action_str)
  ledger.append(summary_str)

  f = open('../log/ledger.ldg', 'w')
  f.writelines(ledger)
  f.close

  return

def authenticate():
  api_key = ""
  f = open('../../key.txt', 'r')
  api_sec = f.read().strip()
  f.close()
  return Client(api_key, api_sec)

def strategy(skip, nbuys):
  
  client = authenticate()
  account_id = client.get_primary_account()

  if get_ledger() == 1:
    return 1
  day, balance, buys, btc, cost = get_ledger()

  base = balance / 5
  buy_amt = base / nbuys

  price_obj = client.get_spot_price()
  price = float(price_obj['amount'])

  sold = False
  
  if buys < nbuys:
    
#    client.buy(account_id, amount=str(buy_amt), currency='USD')
    
    btc += buy_amt/price * .99
    cost += buy_amt
    buys += 1

  elif price * btc > cost * 1.04:
     # sell at >= 103%
    
#    client.sell(account_id, amount=str(btc), currency='BTC')
    
    balance = balance - cost + price * btc * 0.99

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy_amt = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True
  elif price * btc >= cost * 1.01 and cost > balance * .6:
     # sell at >= 100%
    
#    client.sell(account_id, amount=str(btc), currency='BTC')
    
    balance = balance - cost + price * btc * 0.99

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy_amt = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True
  elif price * btc > cost * 0.96 and cost > balance * .8:
     # sell at > 95%
    
#    client.sell(account_id, amount=str(btc), currency='BTC')
    
    balance = balance - cost + price * btc * 0.99

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy_amt = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True

  elif cost + buy_amt < balance:
    
#    client.buy(account_id, amount=str(buy_amt), currency='USD')
    
    btc += buy_amt/price * 0.99
    cost += buy_amt
    buys += 1
    print("Cost : " + str(cost) + "; Day : " + str(day))
  
  if sold:
    action = 'sell'
  else:
    action = 'buy'
  ledger_list = [day+skip, balance, buys, btc, cost, action, buy_amt]
  write_ledger(ledger_list)

  return balance

def main(argv):
  skip = int(argv[1])
  nbuys = int(argv[2])
  strategy(skip, nbuys)
  return 0

if __name__ == '__main__':
  main(sys.argv)
