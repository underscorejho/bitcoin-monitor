#!/usr/bin/python

# Jared Henry Oviatt

# Testing strategies

from urllib.request import urlopen
import sys

def get_csv():
  url = "https://api.bitcoinaverage.com/history/USD/per_day_all_time_history.csv"
  response = urlopen(url).read().decode('utf-8')
  data = response.splitlines()

  prices = []
  for each in data[1:]:
    split = each.split(',')
    prices.append(float(split[3]))
  return prices

def open_csv():
  filename = 'per_day_all_time_history.csv'
  f = open(filename, 'r')
  data = f.readlines()
  prices = []
  for each in data[1:]:
    split = each.split(',')
    prices.append(float(split[3]))
  f.close()
  return prices

def test_1(skip, nbuys):
  sold = False
  buys = 0
  count = 0

  btc = 0.0
  cost = 0.0

  principle = 1000.0
  base = principle / 5
  buy = base / nbuys

  price = open_csv()
  price = price[1000:]
  
  while count < 1000:
    #print("while1")
    while not sold and count < 1000:
      #print("while2")
      while buys < nbuys:
        #print("while3")
        btc += buy/min(price[count:count+skip])
        #btc += buy/price[count]
        cost += buy
  
        buys += 1
        count += skip # every three days
      if price[count] * btc > cost * 1.05:
         # sell at 105%
        principle = principle - cost + price[count] * btc
  
         # reset
        btc, cost, buys = 0, 0, 0
        base = principle / 5
        buy = base / nbuys

        print("-SOLD-\nTotal : " + str(principle) + "\nDay : " + str(count) + "\n")
  
        sold = True
  
      elif price[count] * btc > cost * 1.03:
         # sell at 103%
        principle = principle - cost + price[count] * btc
  
         # reset
        btc, cost, buys = 0, 0, 0
        base = principle / 5
        buy = base / nbuys

        print("-SOLD-\nTotal : " + str(principle) + "\nDay : " + str(count) + "\n")
  
        sold = True
      elif price[count] * btc >= cost and cost > principle / 2:
         # sell at 101%
        principle = principle - cost + price[count] * btc
  
         # reset
        btc, cost, buys = 0, 0, 0
        base = principle / 5
        buy = base / nbuys

        print("-SOLD-\nTotal : " + str(principle) + "\nDay : " + str(count) + "\n")
  
        sold = True
      elif price[count] * btc > cost * 0.95 and cost > principle * .9:
         # sell at 95%
        principle = principle - cost + price[count] * btc
  
         # reset
        btc, cost, buys = 0, 0, 0
        base = principle / 5
        buy = base / nbuys

        print("-SOLD-\nTotal : " + str(principle) + "\nDay : " + str(count) + "\n")
  
        sold = True
      elif cost + buy < principle: # buy
        btc += buy/min(price[count:count+skip])
        #btc += buy/price[count]
        cost += buy
        buys += 1
        print("Cost : " + str(cost) + "; Day : " + str(count))
  
      count += skip # every three days
    sold = False

  return principle

def main(argv):
  test_1(int(argv[1]), int(argv[2]))
  return 0

if __name__ == '__main__':
  main(sys.argv)
