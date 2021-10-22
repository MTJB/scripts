#!/usr/bin/env python3
import argparse
import os
import sys

import docker

dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.extend([dir])
from utils import SqlUtils

docker_cl = docker.from_env()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='''
    Execute SQL against a named MSSQL Docker image.

    This script requires MSSQL to be installed
    and correctly configured.
    https://marktjbrown.com/running-microsoft-sql-server-on-a-mac 
    ''')

    parser.add_argument('--image', dest="sql_image", type=str, help='Name of MSSQL image', default='mssql')
    parser.add_argument('--db-name', '-db', help='Database name', dest="db_name")
    parser.add_argument('--sa-password', '-p', help='Password for the SA account', dest="db_password", required=True)

    # Only one of the following allowed - Query text, or a file
    restore_group = parser.add_mutually_exclusive_group()
    restore_group.add_argument('--sql', '-s', dest="sql", type=str,
                               help='Query text to execute')
    restore_group.add_argument('--sql-file', '-f', dest="sql_file", type=str,
                               help='Path to a .sql file to execute')

    return parser.parse_args()


def execute_sql(args):
    if args.sql is not None:
        text = args.sql
    elif args.sql_file is not None:
        with open(args.sql_file) as f:
            text = f.read()
    else:
        print("You must specify some SQL to run!")
        sys.exit(1)

    SqlUtils.exec_sql_ok(sql_image=args.sql_image,
                         sql=text,
                         show_log=True
                         )


def main():
    global docker_cl
    args = parse_args()
    execute_sql(args=args)


if __name__ == "__main__":
    main()
