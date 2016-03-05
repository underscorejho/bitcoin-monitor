
#!/usr/bin/python

# Jared Henry Oviatt

from urllib.request import urlopen
import math
import sqlite3

  #################

  # Average cost strategy
  # Average Cost:
  # - Buy when price drops below 90% previous week average
  # - Buy $50 at a time
  # - Record each buy price, average price
  # - Sell $250 when price > average buy price
  # 
  # OPTIMIZATION
  # 
  # Optimize buy times:
  # - Set threshold at 80-100% previous week average
  # 
  # Optimize sell times:
  # - Only sell if price >= 110% cost average

  #################
  
  # if sell price is >= 110% avg buy price, sell
  
  # find previous week average

def get_csv():
  url = "https://api.bitcoinaverage.com/history/USD/per_hour_monthly_sliding_window.csv"
  response = urlopen(url).read().decode('utf-8')
  data = response.splitlines()
  return data


def get_sell_threshold():
  conn = sqlite3.connect('bitcoin.db')
  c = conn.cursor()
 
  c.execute('SELECT price FROM transactions')
  values = c.fetchall()

  avg = 0
  for value in values[-5:]:
    avg += value[0]
  avg /= 5
  threshold = 1.05 * avg
 
  c.close()
  conn.close()
  
  threshold = "Sell Threshold: $" + str(threshold) + "\nLimit: $" + str(avg)
  return threshold

def get_buy_threshold():
  month = get_csv()
  total = 0
  for hour in month[-168:]:
    total += float(hour[-6:])

  threshold = .975 * total / 168
  threshold = "Buy Threshold: $" + str(threshold)
  return threshold

def main():
  print(get_buy_threshold())
  print(get_sell_threshold())
  
  return 0

if __name__ == '__main__':
  main()
  


