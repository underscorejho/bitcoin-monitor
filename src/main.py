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
## factor in coinbase fees
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
# Retrieve and read ledger file into variables day, balance, buys, btc, cost 
  # Check if ledger exists or a new one is needed
  if not os.path.isfile('../log/ledger.ldg'):
    print("ERROR: new ledger file is needed.\nCopy new_ledger.ldg into log/ledger.ldg and update balance.\n")
    return 1
  f = open('../log/ledger.ldg', 'r')
  ledger = f.readlines()
  f.close
  
  state = ledger[-1].split(',')
  state = [x.strip() for x in state]
  
  # Returns variables in order
  return int(state[0][5:]), float(state[1][10:]), int(state[2][6:]), float(state[3][5:]), float(state[4][13:])

def write_ledger(ledger_list):
# Replace old ledger file with new file after run
# Writes a human readable ledger/log of transactions
  # ledger_list = [day+1, balance, buys, btc, cost, action, amount]

  # build ledger string if trader bought btc
  buy_str = 'Day: ' + str(ledger_list[0]) + ', Bought $' + str(ledger_list[6]) + '\n' 

  # build ledger string if trader sold btc
  sell_str = 'Day: ' + str(ledger_list[0]) + ', Sold $' + str(ledger_list[6]) + 'for ' + str(ledger_list[4]/ledger_list[6]) + '% profit' + '\n'

  # build ledger string to summarize current state
  summary_str = 'Day: ' + str(ledger_list[0]) + ', Balance: $' + str(ledger_list[1]) + ', Buys: ' + str(ledger_list[2]) + ', BTC: ' + str(ledger_list[3]) + ', Investment: $' + str(ledger_list[4]) + '\n'

  # Chooses appropriate string
  if not ledger_list[5]:
    action_str = buy_str
  else: 
    action_str = sell_str

  # Writes to file
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
# Coinbase authentication
  f = open('../pubkey.txt', 'r')
  api_key = f.read().strip()
  f.close()
  f = open('../key.txt', 'r')
  api_sec = f.read().strip()
  f.close()
  return Client(api_key, api_sec)

def strategy(skip, nbuys):
# This function does the heavy lifting
# Buys and sells based on the state of accounts
  
  client = authenticate()
  account_id = client.get_primary_account()

  # check if ledger exists
  if get_ledger() == 1:
    return 1
  # read ledger into file
  day, balance, buys, btc, cost = get_ledger()

  # initial investment is 20% of current bank balance
  # balance isn't updated until btc is sold
  base = balance / 5
  # each buy is calculated
  buy_amt = base / nbuys

  # get current price from Coinbase API
  price_obj = client.get_spot_price()
  price = float(price_obj['amount'])

  # default is that you aren't selling
  sold = False
  
  # buys chunks until the given limit (nbuys) is reached
  if buys < nbuys:
    
    client.buy(account_id, amount=str(buy_amt), currency='USD')
    
    btc += buy_amt/price * .99 # .99 is to account for 1% Coinbase charge
    cost += buy_amt # keeping track of investment (cost)
    buys += 1

  # begins to try to sell at 4% profit (minus 1% coinbase fee) or more
  elif price * btc > cost * 1.04:
     # sell at >= 103%
    
    client.sell(account_id, amount=str(btc), currency='BTC')
    
    balance = balance - cost + price * btc * 0.99 # updates account balance for ledger if sold

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy_amt = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True

  # trys to sell at 1% profit (minus 1% coinbase fee) or more
  elif price * btc >= cost * 1.01 and cost > balance * .6:
     # sell at >= 100%
    
    client.sell(account_id, amount=str(btc), currency='BTC')
    
    balance = balance - cost + price * btc * 0.99 # updates account balance for ledger if sold

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy_amt = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True

  # trys to sell at 4% loss (minus 1% coinbase fee) or better
  elif price * btc > cost * 0.96 and cost > balance * .8:
     # sell at > 95%
    
    client.sell(account_id, amount=str(btc), currency='BTC')
    
    balance = balance - cost + price * btc * 0.99 # updates account balance for ledger if sold

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy_amt = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True

  # if current sell option isn't possible, continue to buy btc
  elif cost + buy_amt < balance:
    
    client.buy(account_id, amount=str(buy_amt), currency='USD')
    
    btc += buy_amt/price * 0.99
    cost += buy_amt
    buys += 1
    print("Cost : " + str(cost) + "; Day : " + str(day))
  
  # pass shit to write_ledger() and write the ledger
  ledger_list = [day+skip, balance, buys, btc, cost, sold, buy_amt]
  write_ledger(ledger_list)

  return balance

def main(argv):
  skip = int(argv[1])
  nbuys = int(argv[2])
  strategy(skip, nbuys)
  return 0

if __name__ == '__main__':
  main(sys.argv)
