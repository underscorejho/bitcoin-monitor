
#!/usr/bin/python

# Jared Henry Oviatt
# Monitor Bitcoin value and report it
# Recommend action: Buy, Sell, or Nothing

import json
from urllib.request import urlopen
import math
import sqlite3


money = 100.0

def get_json():
  url = "https://api.bitcoinaverage.com/ticker/global/USD/"
  response = urlopen(url).read().decode('utf-8')
  data = json.loads(response)
  return data

def find_change(data):
  conn = sqlite3.connect('bitcoin.db')
  c = conn.cursor()
  
  values = c.execute('SELECT value FROM bitcoin;')
  
  last_value = values.fetchone()
  curr_value = data['last']

  c.close()
  conn.close()
  return curr_value - last_value[0]
  

  return

def analyse(data):
  
  # $ <- B when high
  # $ -> B when low
  
  # move 5% of $
  # if 1% $ < change in value; do nothing
  ## if 20%*5%*$< ^^^ ; do nothing (same as above)
  
  move = .05 * money
  cost = .01 * money
  change = find_change(data)
  
  if math.fabs(change) < cost:
    print("Do Nothing: Change (" + str(change) + ") < Cost (" + str(cost) + ")")
    return -1
  elif change < 0: 
    # $ -> B
    print("Move $" + str(move) + " to Bitcoin: Change = " + str(change))
    return 0
  elif change > 0: 
    # $ <- B
    print("Move $" + str(move) + " to USD: Change = +" + str(math.fabs(change)))
    return 1
  else:
    print("ERROR: Wut")
    return 99

def print_data(data):
  for x, y in data.items():
    print(x, ' : ', y)

def choose_action(action):
  if action == -1:
    choice = 'nothing'
  elif action == 0:
    choice = 'buy'
  elif action == 1:
    choice = 'sell'
  else:
    print('ERROR: Wut')
    return 99
  return choice

def update_db(data, action):
  conn = sqlite3.connect('bitcoin.db')
  c = conn.cursor()

  time = data['timestamp'].replace(',', '')
  time = time.replace(' ', '-')

  value = data['last']
  
  action = choose_action(action)

  c.execute("INSERT INTO bitcoin VALUES (?,?,?)", (time, value, action))
  print("Adding row to db:\n" + time + "|" + str(value) + "|" + action)
  
  conn.commit()
  c.close()
  conn.close()
  return 0

def main():
  data = get_json()
  action = analyse(data)

  print_data(data)
  
  update_db(data, action)

  return 0

if __name__ == '__main__':
  main()
  


