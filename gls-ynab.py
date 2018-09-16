#!/usr/bin/env python3
import sys
import pandas as pd

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if len(sys.argv) != 2:
	eprint("Usage: ./gls-ynab.py input.csv")
	sys.exit(1)

source_file = sys.argv[1]
eprint("Reading from file " + source_file)

df = pd.read_csv(source_file,
                 encoding="cp1252",
                 delimiter=";",
                 parse_dates=['Buchungstag', 'Wertstellung'],
                 dayfirst=True,
                 decimal=',',
                 thousands='.',
                 float_precision='high')

df1 = df.drop(['Wertstellung', 'Kontonummer', 'Buchungstext', 'Kontostand', 'Währung'], axis=1)
df1.rename(columns={'Auftraggeber/Empfänger': 'Payee', 'Buchungstag': 'Date'}, inplace=True)
df1 = df1.set_index('Date')

def merge_vwzs(row):
    vwzs_with_value = [str(col) for col in row if type(col) is str]
    return ' '.join(vwzs_with_value)

df2 = df1.copy()
vwzs = list(filter(lambda x: x.startswith('VWZ'), df.columns))
df2['Memo'] = df1[vwzs].apply(lambda x: merge_vwzs(x), axis=1)
df2 = df2.drop(vwzs, axis=1) 

df3 = df2.copy()
df3['Outflow'] = df3['Betrag'].apply(lambda x: -x if x < 0 else 0)
df3['Inflow'] = df3['Betrag'].apply(lambda x: x if x >= 0 else 0)
df3 = df3.drop('Betrag', axis=1)

print(df3.to_csv())