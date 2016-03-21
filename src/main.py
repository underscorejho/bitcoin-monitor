
#!/usr/bin/python

# Jared Henry Oviatt

from urllib.request import urlopen
import sqlite3

  #################

  # Average cost strategy
  # Average Cost:
  # - Buy when price drops below 97% previous week average
  # - Buy $50 at a time
  # - Record each buy price, average price
  # - Sell $250 when price > 105% average buy price
   
  #################
  
def get_csv():
  url = "https://api.bitcoinaverage.com/history/USD/per_hour_monthly_sliding_window.csv"
  response = urlopen(url).read().decode('utf-8')
  data = response.splitlines()
  return data

def get_sell_threshold():
  conn = sqlite3.connect('../db/bitcoin.db')
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
  
  print("Sell Threshold: $" + str(threshold) + "\nLimit: $" + str(avg))
  return threshold

def get_buy_threshold():
  month = get_csv()
  total = 0
  for hour in month[-168:]:
    total += float(hour[-6:])

  threshold = .975 * total / 168
  print("Buy Threshold: $" + str(threshold))
  return threshold

def main():
  get_buy_threshold()
  get_sell_threshold()
  return 0

if __name__ == '__main__':
  main()
  


