-- Source database name
DECLARE @SRC NVARCHAR(50)='TEST'
-- Target filename
DECLARE @TRG NVARCHAR(200)='/tmp/'+@SRC+'.bak'

DECLARE @TRUNCATE_TXN_LOG BIT=0

IF @TRUNCATE_TXN_LOG=1
    BEGIN

        DECLARE @LOG_FILE NVARCHAR(MAX)
        DECLARE @stmt VARCHAR(MAX)
        DECLARE @SET_RECOVERY_MODE VARCHAR(MAX)= 'ALTER DATABASE '+@SRC+'SET RECOVERY {RECOVERY_MODE}'
        DECLARE @SHRINK VARCHAR(MAX)= 'DBCC SHRINKFILE ({LOG_FILE}, 1)'

        SELECT @LOG_FILE = (
            SELECT name
            FROM sys.master_files
            WHERE database_id = (SELECT database_id FROM sys.databases WHERE name = @SRC)
            AND type = 1 /* type=1 ≡ log file */
        )

        PRINT 'Shrinking transaction Log: ' + @LOG_FILE
        SELECT @stmt = REPLACE(@SET_RECOVERY_MODE, '{RECOVERY_MODE}', 'SIMPLE')
        EXEC (@stmt)

        SELECT @stmt = REPLACE(@SHRINK, '{LOG_FILE}', @LOG_FILE)
        EXEC (@stmt)

        SELECT @stmt = REPLACE(@SET_RECOVERY_MODE, '{RECOVERY_MODE}', 'FULL')
        EXEC (@stmt)
    END

USE [master]
-- Rebuild indexes using AdaptiveIndexDefrag https://github.com/microsoft/tigertoolbox/tree/master/AdaptiveIndexDefrag
use msdb
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'usp_AdaptiveIndexDefrag') BEGIN
    PRINT 'Rebuilding indexes - this may take a while if your db is bad'
    -- NB, if running this again later, don't need all the params, just @dbScope if you want to run on just one db
    EXEC msdb.dbo.usp_AdaptiveIndexDefrag @dbScope = @SRC, @onlineRebuild = 0, @defragDelay='0s', @sortInTempDB=1 -- @forceRescan=1,
END ELSE 
PRINT 'AdaptiveIndexDefrag not installed - you should probably install it from https://github.com/microsoft/tigertoolbox/tree/master/AdaptiveIndexDefrag'

DECLARE @BACKUP VARCHAR(MAX)= 
'BACKUP DATABASE ['+@SRC+'] TO DISK = '''+@TRG+''' WITH NOFORMAT, INIT,  NAME = '''+@SRC+''', NOSKIP, REWIND, NOUNLOAD,  STATS = 10'

--SELECT @BACKUP
EXEC (@BACKUP)
