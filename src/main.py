#!/usr/bin/python

# Jared Henry Oviatt


########
#
# TODO:
# get accurate prices with Coinbase
# write ledger to file on run
# use ledger to keep track of buys/sells instead of db
# read day and balance from ledger
# ... 'Day: 5, Bought .xx BTC for $xx.xx' OR 'Day: 5, Sold x.xx BTC for $xxx.xx at xxx.xx% profit
# ... 'Day: 5, Balance: $5000, Buys: 3, BTC: .23, Investment: $105'
# set cron job to run daily
# run on every 5th/10th day
# deposit 'deposit' every 30th day
# set up email notification reporting results (python main > mailto...)
# ... action - (buy $xxx.xx today OR (if past nbuys) sell at $xxx.xx for xxx% profit)
# ... deposit - (deposit $xx.xx today)
# ... total - (total account starting with $1000.00: $xxxx.xx)
#
########

from urllib.request import urlopen
import sys


def strategy(skip, nbuys):
  
  day, balance, buys, btc, cost = get_ledger()

  base = balance / 5
  buy = base / nbuys

  price = # something from coinbase

  if buys = 0:
    sold = False
  
###  Change to buy algorithm
  if buys < nbuys:
    btc += buy/price
    cost += buy
    buys += 1
    day += skip
###

###  Change to sell algorithm
  if price * btc > cost * 1.03:
     # sell at >= 103%
    balance = balance - cost + price * btc

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True
  elif price * btc >= cost and cost > balance * .6:
     # sell at >= 100%
    balance = balance - cost + price * btc

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True
  elif price * btc > cost * 0.95 and cost > balance * .8:
     # sell at > 95%
    balance = balance - cost + price * btc

     # reset
    btc, cost, buys = 0, 0, 0
    base = balance / 5
    buy = base / nbuys

    print("-SOLD-\nTotal : " + str(balance) + "\nDay : " + str(day) + "\n")
    ledger.append("Total : " + str(balance) + "; Day : " + str(day) + "")

    sold = True
###

###
  elif cost + buy < balance:
    btc += buy/price
    cost += buy
    buys += 1
    print("Cost : " + str(cost) + "; Day : " + str(day))
###
  
  write_ledger(day+1, balance, buys, btc, cost)

  return balance

def main(argv):
  skip = int(argv[1])
  nbuys = int(argv[2])
  strategy(skip, nbuys)
  return 0

if __name__ == '__main__':
  main(sys.argv)
