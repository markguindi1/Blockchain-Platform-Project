#!/usr/bin/env python3
import sys

#
#  Downgrades pg_dump 10 script to 9.x
#  removing 'AS integer' from 'CREATE SEQUENCE' statement
#
#  Usage:
#       $ python3 pgdump_10_to_9.py < test10.sql > test9.sql
#  or:
#       $ cat test10.sql | ./pgdump_10_to_9.py > test9.sql
#
#  To obtain a compressed 9.x sql script from a compressed 10 sql script:
#
#       $ gunzip -c test10.sql.gz | ./pgdump_10_to_9.py | gzip > test9.sql.gz
#

inside_create_sequence = False
for row in sys.stdin.readlines():

    if inside_create_sequence and row.strip().lower() == 'as integer':
        pass
    else:
        print(row, end='', flush=True)

    inside_create_sequence = row.strip().startswith('CREATE SEQUENCE ')

