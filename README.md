# Scripts
Random collection of scripts I sometimes use, and some I didn't want to lose 🤷

**DISCLAIMER:** Worked on my machine (at one point, maybe)

## List of scripts in this repository

* setupDb.py - Create a new MSSQL image, installing some helpful extras.

### [Database](database)
* [backupDatabase.sql](database/backupDatabase.sql) - TSQL script to shrink DB log file, defrag indexes, and take a db backup. 
* [checkQueryCache.sql](database/checkQueryCache.sql) - TSQL script to check slow running queries via MSSQL [DMVs](https://docs.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/system-dynamic-management-views?view=sql-server-ver15). 
