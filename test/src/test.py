#!/usr/bin/python

# Jared Henry Oviatt

# Testing strategies

from urllib.request import urlopen
import sys

def get_csv():
# Downloads up to date historical data
  url = "https://api.bitcoinaverage.com/history/USD/per_day_all_time_history.csv"
  response = urlopen(url).read().decode('utf-8')
  data = response.splitlines()

  prices = []
  for each in data[1:]:
    split = each.split(',')
    prices.append(float(split[3]))
  return prices

def open_csv():
# Opens generated fake historical data
# Generate data with fake_data.py
  filename = '../csv/fake_prices.csv'
  f = open(filename, 'r')
  data = f.readlines()
  prices = []
  for each in data:
    prices.append(float(each))
  f.close()
  return prices

def test_1(skip, nbuys, deposit):
# Runs strategy (same as main) on data
# sorry I know this bits messy
  sold = False
  buys = 0
  count = 0

  btc = 0.0
  cost = 0.0

  principle = 1000.0
  base = principle / 5
  buy = base / nbuys

  price = open_csv()
  
  ledger = []
  
  while count < 3400: # 3400 is almost 10 years; weird numbers to keep things in range
    while not sold and count < 3400:
      while buys < nbuys and count < 3400:
        #btc += buy/min(price[count:count+skip])
        btc += buy/price[count] * .99
        cost += buy
        buys += 1
        count += skip
      if count % 30 == 0 and deposit:
        principle += deposit
        print("Deposit: " + str(deposit) + "; Day: " + str(count))

      if price[count] * btc > cost * 1.04:
         # sell at 103%
        principle = principle - cost + price[count] * btc * .99
  
         # reset
        btc, cost, buys = 0, 0, 0
        base = principle / 5
        buy = base / nbuys

        print("-SOLD-\nTotal : " + str(principle) + "\nDay : " + str(count) + "\n")
        ledger.append("Total : " + str(principle) + "; Day : " + str(count) + "")
  
        sold = True
      elif price[count] * btc >= cost * 1.01 and cost > principle * .6:
         # sell at 100%
        principle = principle - cost + price[count] * btc * .99
  
         # reset
        btc, cost, buys = 0, 0, 0
        base = principle / 5
        buy = base / nbuys

        print("-SOLD-\nTotal : " + str(principle) + "\nDay : " + str(count) + "\n")
        ledger.append("Total : " + str(principle) + "; Day : " + str(count) + "")
  
        sold = True
      elif price[count] * btc > cost * 0.96 and cost > principle * .8:
         # sell at 95%
        principle = principle - cost + price[count] * btc * .99
  
         # reset
        btc, cost, buys = 0, 0, 0
        base = principle / 5
        buy = base / nbuys

        print("-SOLD-\nTotal : " + str(principle) + "\nDay : " + str(count) + "\n")
        ledger.append("Total : " + str(principle) + "; Day : " + str(count) + "")
  
        sold = True
      elif cost + buy < principle:# and cost < principle * .6: # buy
        #btc += buy/min(price[count:count+skip])
        btc += buy/price[count] * .99
        cost += buy
        buys += 1
        print("Cost : " + str(cost) + "; Day : " + str(count))
  
      count += skip
      if count % 30 == 0 and deposit:
        principle += deposit
        print("Deposit: " + str(deposit) + "; Day: " + str(count))
    sold = False
    
  print("\n\n----------DONE----------\nSummary: Skip " + str(skip) + " Buy " + str(1/nbuys/5) + " principle * " + str(nbuys))
  for each in ledger:
    print(each)

  return principle

def main(argv):
  skip = int(argv[1])
  nbuys = int(argv[2])
  deposit = 0
  if len(argv) > 3:
    deposit = float(argv[3])
  test_1(skip, nbuys, deposit)
  return 0

if __name__ == '__main__':
  main(sys.argv)
