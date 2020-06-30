import holdings as h

h.new_db()
h.update_db('2020-05-25', 'S&P500', 'TICKER', 1198.39, 'KRISTAL')
h.update_db('2020-05-12', 'IWDA', 'TICKER', 2081.26, 'KRISTAL')
h.update_db('2020-06-10', 'VWO', 'TICKER', 1128.05, 'KRISTAL')
h.update_db('2019-06-01', 'SSB', '1.0', 1000, 'FIXED')
h.update_db('2020-06-10', 'STI ETF', 'TICKER', 3376.8, 'VICKERS')
h.ls_db()