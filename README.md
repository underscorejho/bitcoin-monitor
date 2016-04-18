# bitcoin-trader-jho

Uses a dollar-cost averaging based strategy to automatically buy and sell bitcoin.
Run on a cron job (with command `python trader.py x y`) every y day.

Includes testing programs `test.py` and `fake_data.py` to generate fake data or pull historical data and run different strategies over this data.

Also includes (deprecated)(shitty database exercise) transactions.py for keeping track of bitcoin transactions.
