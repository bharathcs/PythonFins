import sqlite3
import pandas as pd
import datetime as dt

dbpath = "holdings.db"
columns_heading = ['TxID', 'TxDate', 'Name','Ticker','Amount', 'Broker']

def new_db():
    with open(dbpath, 'w'):
        db = sqlite3.connect(dbpath)

    db.execute("""DROP TABLE IF EXISTS holdings;""")

    db.execute('''CREATE TABLE holdings(
            TxID INTEGER NOT NULL,
            TxDate DATE ,
            Name VARCHAR(50),
            Ticker VARCHAR(25),
            Amount DECIMAL(10,2),
            Broker VARCHAR(25),
            PRIMARY KEY (TxID)
        );
        ''')
    db.commit()
    db.close()

def update_db(txdate, name, ticker, amount, broker):
    db = sqlite3.connect(dbpath)

    db.execute("INSERT into holdings (TxDate, Name, Ticker, Amount, Broker) \
        VALUES (?, ?, ?, ?, ?)", (txdate, name, ticker, amount, broker))
    
    db.commit()
    db.close()

def ls_db():
    '''Returns as a panda dataframe the contents of holdings.db
    '''
    db = sqlite3.connect(dbpath)
    dictarr = []
    
    result = db.execute("SELECT * FROM holdings")
    for row in result:
        dict1 = {}
        for i, column in enumerate(columns_heading):
            dict1[column] = row[i]
        dictarr.append(dict1)
    
    df = pd.DataFrame(dictarr)
    df.set_index('TxID')
    return df

def arr_holdings():
    '''Returns all holdings as instances of class Holdings
    '''
    arr_holdings = []
    df = ls_db()
    holding_names = df.Name.unique()
    for name in holding_names:
        temp_df = df[df.Name == name]
        ticker = temp_df.Ticker.unique()
        broker = temp_df.Broker.unique()
        if (len(ticker) == 1 and len(broker) == 1):
            holding = Holdings(name, ticker[0], broker[0])
        else:
            print(name, ticker, broker)
            raise Exception("Database has multiple tickers / brokers for this name")
        
        dates = temp_df.to_dict()['TxDate']
        amounts = temp_df.to_dict()['Amount']
        print(list(zip(dates.values(), amounts.values())))
        holding.update_trades(list(zip(dates.values(), amounts.values())))

        arr_holdings.append(holding)
    return arr_holdings

def new_tx(new_trade):
    """Takes in ["DD-MM-YYY, Float_amount] and turns it into datetime.date object
    Also checks that it is before today.
    """
    try:
        assert(len(new_trade) == 2)
        tx_date = dt.date.fromisoformat(new_trade[0])
        amt = float(new_trade[1])
    except:
        raise Exception(
            "Transaction must be in list format as"
            + " an array of string (valid date of transaction"
            + " before today) and float (amount invested):"
            + " [YYYY-MM-DD, amount]."
    )
    return [tx_date, amt]

class Holdings:
    def __init__(self, name, ticker, broker):
        self.name = name
        self.ticker = ticker
        self.broker = broker
        self.trades = []
    
    def ls_trades(self):
        print("Date        |     Amount\t")
        print("------------------------\t")
        for row in self.trades:
            date = str(row[0])
            amt = int(round(row[1],0))
            amt = f'{amt:,}'
            print("{0}   ${1:>10}\t".format(date, amt))
        print()

    def update_trades(self, updated_trades):
        newlist = []
        if type(updated_trades) != list:
            raise Exception("trades should be in list format")
        for row in updated_trades:
            newlist.append(new_tx(row))
        self.trades = newlist
    
    def new_trade(self, new_trade):
        self.trades.append(new_tx(new_trade))

# TESTING