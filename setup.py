#!/usr/bin/env python3
import argparse

import docker
import requests
from docker.errors import NotFound

from utils import SqlUtils

docker_cl = docker.from_env()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='''
    Install Stored Procedures used within this directory
    onto a named MSSQL Docker image.

    This script requires MSSQL to be installed
    and correctly configured.
    https://marktjbrown.com/running-microsoft-sql-server-on-a-mac 
    ''')

    parser.add_argument('--image', dest="sql_image", type=str, help='Name of MSSQL image', default='mssql')
    parser.add_argument('--db-image-version', '-v', dest="db_image_version", help='MSSQL version to install',
                        default="2017")
    parser.add_argument('--db-name', '-db', help='Database name', dest="db_name")
    parser.add_argument('--sa-password', '-p', help='Password for the SA account', dest="db_password", required=True)
    parser.add_argument('--db-only', dest="db_only", action='store_true',
                        help='Only install MSSQL image, if not exists')

    return parser.parse_args()


def start_mssql_docker(args):
    global docker_cl
    try:
        mssql = docker_cl.containers.get(args.sql_image)
        if mssql.status != "running":
            mssql.start()
    except docker.errors.NotFound:
        sql_img = f"mcr.microsoft.com/mssql/server:{args.db_image_version}-latest"
        print("Starting new SQLServer with image {}".format(sql_img))
        docker_cl.images.pull(sql_img)
        docker_cl.containers.run(sql_img, name=args.sql_image,
                                 ports={'1433/tcp': 1433}, auto_remove=False, detach=True,
                                 restart_policy={"Name": "always"},
                                 environment={"ACCEPT_EULA": "Y", "SA_PASSWORD": args.db_password}
                                 )


def install_adaptive_index_defrag(args):
    url = 'https://raw.github.com/microsoft/tigertoolbox/master/AdaptiveIndexDefrag/usp_AdaptiveIndexDefrag.sql'
    r = requests.get(url)
    SqlUtils.exec_sql_ok(sql_image=args.sql_image,
                         sql=r.text,
                         show_log=False
                         )
    print(f'Installed AdaptiveIndexDefrag from {url}!')


def install_who_is_active(args):
    url = 'https://raw.github.com/amachanic/sp_whoisactive/master/who_is_active.sql'
    r = requests.get(url)
    SqlUtils.exec_sql_ok(sql_image=args.sql_image,
                         sql=r.text,
                         show_log=False
                         )
    print(f'Installed dbo.sp_WhoIsActive from {url}!')


def main():
    global docker_cl
    args = parse_args()
    start_mssql_docker(args=args)
    if not args.db_only:
        install_adaptive_index_defrag(args=args)
        install_who_is_active(args=args)


if __name__ == "__main__":
    main()
