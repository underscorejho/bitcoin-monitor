
#!/usr/bin/python

# Jared Henry Oviatt
# Record Bitcoin Transactions

import sqlite3
import time

def get_info():
  a = 0
  while a == 0:
    answer = input("Did you BUY or SELL? (BUY/SELL)\n")
    if answer.lower().strip() == 'buy':
      action = "BUY"
      amount = int(input("What dollar amount did you buy?\n"))
      price = int(input("What was the price when you bought?\n"))
      a = 1
    elif answer.lower().strip() == 'sell':
      action = "SELL"
      amount = int(input("What dollar amount did you recieve?\n"))
      price = int(input("What was the price when you sold?\n"))
      a = 1
    else:
      print("Bad input, try again\n")

  return action, amount, price

def record(action, amount, price):
  conn = sqlite3.connect('bitcoin.db')
  c = conn.cursor()
 
  c.execute("INSERT INTO transactions VALUES (?,?,?,?)", (time.strftime('%c'), action, amount, price))
  print("Adding row to db:\n" + time.strftime('%c') + "|" + action + "|" + str(amount) + "|" + str(price))

  conn.commit()
  c.close()
  conn.close()
 
  return 0

def main():
  answer = input("Add transaction record? (y/n)\n")
  if answer.lower().strip() != 'y':
    print("Bye")
    return 0

  action, amount, price = get_info()

  record(action, amount, price)

  return 0

if __name__ == '__main__':
  main()
