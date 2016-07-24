# -*- coding: utf-8 -*-

import petl as etl
import csv
import psycopg2

# set up a CSV file to demonstrate with
def test_etl_csv():
    table1 = [['foo', 'bar'],
              ['a', 1],
              ['b', 2],
              ['c', 2]]
    with open('example.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table1)

    # now demonstrate the use of fromcsv()
    table2 = etl.fromcsv('example.csv')
    print(table2)

def test_extract_db():
    connection = psycopg2.connect('dbname=stock user=stock password=stock')
    table = etl.fromdb(connection, 'SELECT * FROM quotes')
    print(table)

def test_load_db():
    raw_file = 'tse_with_header.csv'
    tse = etl.fromcsv(raw_file)
    connection = psycopg2.connect('dbname=stock user=stock password=stock')

    # assuming table "quotes" already exists in the database, and tse need to have the header.
    # petl.io.db.todb(table, dbo, tablename, schema=None, commit=True, create=False, drop=False, constraints=True,
    #                metadata=None, dialect=None, sample=1000)[source]
    etl.todb(tse, connection, 'quotes', drop=False)

def test_tse():
    raw_file = 'tse-(before).csv'
    tse = etl.fromcsv(raw_file)
    print(tse)

if __name__ == '__main__':
    #test_tse()
    print('before load...')
    test_extract_db()
    test_load_db()
    print('after load...')
    test_extract_db()