USE [master]
ALTER DATABASE [{0}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE
RESTORE DATABASE [{0}] FROM  DISK = N'D:\SQL\Backup\dbmCCenterSparrow.bak' WITH  FILE = 1,  MOVE N'dbmCCenterTal_data' TO N'C:\Program Files\Microsoft SQL Server\MSSQL12.INST01\MSSQL\DATA\{0}_data.mdf',  MOVE N'dbmCCenterTal_log' TO N'C:\Program Files\Microsoft SQL Server\MSSQL12.INST01\MSSQL\DATA\{0}_log.ldf',  NOUNLOAD,  STATS = 5
ALTER DATABASE [{0}] SET MULTI_USER

GO


