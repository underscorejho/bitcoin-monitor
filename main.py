
#!/usr/bin/python

# Jared Henry Oviatt

import json
from urllib.request import urlopen
import math
import sqlite3

def get_json():
  url = "https://api.bitcoinaverage.com/ticker/global/USD/"
  response = urlopen(url).read().decode('utf-8')
  data = json.loads(response)
  return data

def get_csv():
  url = "https://api.bitcoinaverage.com/history/USD/per_hour_monthly_sliding_window.csv"
  response = urlopen(url).read().decode('utf-8')
  data = response.splitlines()
  return data

def print_data(data):
  for x, y in data.items():
    print(x, ' : ', y)
  return

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
  
  print("Sell Threshold: $" + str(threshold) + "($" + str(avg) + ")")
  return threshold

def get_buy_threshold(month):
  total = 0
  for hour in month[-168:]:
    total += float(hour[-6:])

  threshold = .975 * total / 168
  print("Buy Threshold: $" + str(threshold))
  return threshold

def update_db(data, action):
  conn = sqlite3.connect('bitcoin.db')
  c = conn.cursor()

  time = data['timestamp'].replace(',', '')
  time = time.replace(' ', '-')

  value = (data['ask'] + data['bid'])/2
  
  c.execute("INSERT INTO bitcoin VALUES (?,?)", (time, value))
  print("Adding row to db:\n" + time + "|" + str(value))
  
  conn.commit()
  c.close()
  conn.close()
  return 0

def main():
  #  now = get_json()
  #  print_data(data)

  month = get_csv()
  
  get_buy_threshold(month)
  get_sell_threshold()
  
  #  update_db(now)

  return 0

if __name__ == '__main__':
  main()
  


