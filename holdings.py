import quandl as q
import pandas as pd
import datetime as dt
import csv

default_currency = 'SGD'
holdings_info_path = 'holdings_info.csv'
transactions_path = 'transactions.csv'

def new_tx(new_trade):
    """Takes in ["DD-MM-YYY, Float_amount, Currency] and turns date into datetime.date object
    Also checks that it is before today.
    """
    try:
        assert(len(new_trade) == 3)
        tx_date = dt.date.fromisoformat(new_trade[0])
        amt = float(new_trade[1])
        shares = new_trade[2]

    except:
        raise Exception(
            "Transaction must be in list format as"
            + " an array of string (valid date of transaction"
            + " before today), float (amount invested) and int"
            + " (number of shares):"
            + " [YYYY-MM-DD, amount, shares]."
    )
    return [tx_date, amt, shares]

class Holdings:
    def __init__(self, name, ticker, broker, currency='SGD'):
        self.name = name
        self.ticker = ticker
        self.broker = broker
        self.currency = currency
        self.trades = []
    
    def ls_trades(self):
        self.sort_trades()
        print(f'{self.name} ({self.ticker} - {self.broker})')
        print("Date        |       Amount\t")
        print("--------------------------\t")
        for row in self.trades:
            date = str(row[0])
            amt = int(round(row[1],0))
            amt = f'{amt:,}'
            print("{0}   {2}{1:>10}\t".format(date, amt, self.currency))
        print()

    def update_trades(self, updated_trades):
        newlist = []
        if type(updated_trades) != list:
            raise Exception("trades should be in list format")
        for row in updated_trades:
            newlist.append(new_tx(row))
        self.trades = newlist
        self.sort_trades()
    
    def new_trade(self, new_trade):
        self.trades.append(new_tx(new_trade))
        self.sort_trades()
    
    def sort_trades(self):
        self.trades.sort(key=lambda x:x[0].isoformat())

def holdings_from_csv():
    arr_holdings = []

    with open(holdings_info_path, 'r') as file:
        csv_holdings_info = csv.reader(file)

        for entry in csv_holdings_info:
            name, ticker, broker = entry[0], entry[1], entry[2]
            currency = entry[3] if len(entry[3]) != 0 else default_currency

            new_entry = Holdings(name, ticker, broker, currency)
            arr_holdings.append(new_entry)

    return arr_holdings

def trades_from_csv(arr_holdings):
    """Takes in array of holdings and for each holding, update trades using the transaction history
    Matches transaction to holdings by their names
    """

    with open(transactions_path, 'r') as file:
        csv_transactions = csv.reader(file)

        for entry in csv_transactions:
            name, date, amount, shares = entry[0], entry[1], entry[2], entry[3]

            for holding in arr_holdings:
                if holding.name != name:
                    continue
                holding.new_trade([date, amount, shares])

    return arr_holdings

arr_holdings = trades_from_csv(holdings_from_csv())
for entry in arr_holdings:
    entry.ls_trades()