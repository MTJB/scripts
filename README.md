# Scripts
Random collection of scripts I sometimes use, and some I didn't want to lose 🤷

**DISCLAIMER:** Worked on my machine (at one point, maybe)

## List of scripts in this repository

### [Database](database)
* [setupDb.py](database/setupDb.py) - Create a new MSSQL image, installing some helpful extras. 
* [backupDatabase.sql](database/backupDatabase.sql) - TSQL script to shrink DB log file, defrag indexes, and take a db backup. 
* [checkIndexFragmentation.sql](database/checkIndexFragmentation.sql) - TSQL script to check index fragmentation on all tables. 
* [checkQueryCache.sql](database/checkQueryCache.sql) - TSQL script to check slow running queries via MSSQL [DMVs](https://docs.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-views/system-dynamic-management-views?view=sql-server-ver15). 
* [monitorForDeadlockEvents.sql](database/monitorForDeadlockEvents.sql) - TSQL to add a new extended event to the server which watches for Deadlocks occurring. 
