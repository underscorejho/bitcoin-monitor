#!/usr/bin/python

# Jared Henry Oviatt

# create raw data

import random

# pull prices from api csv
def parse_csv():
  filename = 'csv/per_day_all_time_history.csv'
  f = open(filename, 'r')
  data = f.readlines()
  prices = []
  for each in data[1:]:
    split = each.split(',')
    prices.append(float(split[3]))
  f.close()

  prices = prices[-1000:]
  
  f = open("csv/prices.csv", "w")
  f.write(str(prices).replace("[", "").replace("]", "").replace(",", "\n").strip())
  f.close()
  
  return prices

def fake_data():
  random.seed()
  count = 0
  value = 200.0
  data = []
  while count <= 3500:
    # increase by rand1 * 10 * rand2 * rand3(+/-) for rand4 times
    rand1 = random.random() * 10
    rand2 = float(random.randint(1, 5))
    rand3 = random.random()
    rand4 = random.randint(1, 10)
    
    # get change
    change = rand1 * rand2 * (rand3 - .5)
    for i in range(0, rand4):
      count += 1
      value += change
      data.append(abs(round(value, 2))+100)

  return data[:3500]

def fake_forex():
  random.seed()
  count = 0
  value = 1.0
  data = []
  while count <= 3500:
    # increase by rand1 * rand2 * rand3(+/-) for rand4 times
    rand1 = random.random()
    rand2 = float(random.randint(10, 200))
    rand3 = random.random()
    rand4 = random.randint(1, 3)
    
    # get change
    change = rand1 / rand2 * (rand3 - .5)
    for i in range(0, rand4):
      count += 1
      if abs(value + change) >= .5 and abs(value + change) <= 1.5:
        value += change
      data.append(abs(round(value, 2)))

  return data[:3500]

def save_fake_data(data):

  f = open("csv/fake_prices.csv", "w")
  f.write(str(data).replace("[", "").replace("]", "").replace(",", "\n").strip())
  f.close()

def main():
  #parse_csv()
  save_fake_data(fake_data())
  #save_fake_data(fake_forex())
  #print(fake_data())
  #print(fake_forex())
  return

if __name__ == '__main__':
  main()
