CREATE OR ALTER PROCEDURE [dbo].[ApplyDataAccessAuditingSettings]
	@auditing_type INT,
	@max_storage_size_suspected INT,
	@max_storage_size_authorized INT,
	@server_principals NVARCHAR(max) = NULL
/******************************************************************************
**      Description:            apply settings for the Audit
**
**      Input Parameter:        @auditing_type: 999 - no audit/0- suspected/1- authorized+suspected
**						        @max_storage_size - max disk space allocated
**                                          
**      Called By:              CCenter
**      PBI Number:             
**
**      External Temp Table:     + 
**      
**      Created By:				Alen          
**      Creation Date:          2021-02-01
**     
*******************************************************************************
 
--      Execution Example: 
--     
        EXEC  @auditing_type = 
 
*******************************************************************************
**      Change History: 
**      --------------
**
**      Date:           Author:         Description:
**      -----------     --------        --------------------------------------
**      2021-02-17     Alex P         new param- @server_principals
*******************************************************************************/
AS
SET NOCOUNT ON
BEGIN
	
	DECLARE @new_max_rollover_files_suspected AS INT,
			@new_max_rollover_files_authorized AS INT,
			@max_rollover_files_suspected AS INT,
			@max_rollover_files_authorized AS INT,
			@is_state_enabled BIT,
			@SUSPICIOUS_ONLY AS INT = 0,
			@SUSPICIOUS_AND_AUTHORIZED AS INT = 1,
			@NO_AUDITING AS INT = 999,
			@sqlServiceAccounts NVARCHAR(max) = ''

	SET @server_principals = NULLIF(RTRIM(LTRIM(@server_principals)),'')

	DROP TABLE IF EXISTS #server_principals
	CREATE TABLE #server_principals (UserName nvarchar(255))

	SELECT  @new_max_rollover_files_suspected = ISNULL(NULLIF(@max_storage_size_suspected, 0), 50)/50,
			@new_max_rollover_files_authorized = ISNULL(NULLIF(@max_storage_size_authorized, 0), 50)/50

	EXEC ('USE master; ALTER SERVER AUDIT [CDR_Authorized] WITH (STATE = OFF);');
	EXEC ('USE master; ALTER SERVER AUDIT [CDR_Suspected] WITH (STATE = OFF);');

	SELECT  @max_rollover_files_authorized = max_rollover_files,
			@is_state_enabled = is_state_enabled
	FROM sys.server_file_audits
	WHERE name = 'CDR_Authorized'

	IF @max_rollover_files_authorized <> @new_max_rollover_files_authorized
		EXEC ('USE master; ALTER SERVER AUDIT [CDR_Authorized]  TO FILE ( MAX_ROLLOVER_FILES =  '+ @new_max_rollover_files_authorized + ');');	
				
	SELECT  @max_rollover_files_suspected = max_rollover_files,
			@is_state_enabled = is_state_enabled
	FROM sys.server_file_audits
	WHERE name = 'CDR_Suspected'

	IF @max_rollover_files_suspected <> @new_max_rollover_files_suspected
		EXEC ('USE master; ALTER SERVER AUDIT [CDR_Suspected]  TO FILE ( MAX_ROLLOVER_FILES =  '+ @new_max_rollover_files_suspected + ');');
	
/* Updating server principals (accounts) list to be filtered from suspected audit and added to authorized audit */

	INSERT INTO #server_principals (UserName) 
	SELECT DISTINCT RTRIM(LTRIM([value]))
	FROM STRING_SPLIT(@server_principals,',')
	WHERE RTRIM(LTRIM([value])) > ''

	DECLARE @isAddAccExists BIT = 1

	-- if the users were removed we should run the ALTER to apply it
	IF NOT EXISTS(SELECT * FROM #server_principals)
	SET @isAddAccExists = 0

	/*CDR_Suspected*/

	/* adding SQL Server service and SQL Server Agent service accounts */
	SELECT @sqlServiceAccounts = @sqlServiceAccounts +  N'session_server_principal_name <>''' + service_account + N''' AND '
	FROM sys.dm_server_services
	GROUP BY service_account

	DECLARE @strSQL NVARCHAR(max) = N'use master; ALTER SERVER AUDIT [CDR_Suspected] WHERE ' + CASE WHEN @isAddAccExists=1 THEN '(' ELSE '' END

	SELECT @strSQL = @strSQL + '[session_server_principal_name] <> ''' + UserName + ''' AND '
	FROM #server_principals

	-- the dbMotion app accounts should be replaced with the system parameters
	SET @strSQL=CASE WHEN @isAddAccExists = 0 THEN @strSQL ELSE LEFT(@strSQL, LEN(@strSQL)-4) + ') AND ' END 
	+ '(' + @sqlServiceAccounts + '[session_server_principal_name]<> ''$DIL_USER_ACCOUNT$'' -- DIL to Stage
	AND [session_server_principal_name]<> ''$DATA_CAG_USER_ACCOUNT$'' -- Retrieve data for CAG
	AND [session_server_principal_name]<> ''$SECURITY_SERVICE_USER_ACCOUNT$'' -- Service account for apps
	AND [session_server_principal_name]<> ''$DATA_DAT_GROUP_ACCOUNT$'' -- User group for DAT queries
	AND [session_server_principal_name]<> ''$DATA_PHA_READER_USER_ACCOUNT$'' -- PHA service account
		AND [session_server_principal_name]<>'''' 
		OR [application_name]<>''Microsoft SQL Server Service Broker Activation'' AND [session_server_principal_name]='''' 
		OR [application_name]=''Microsoft SQL Server Service Broker Activation'' AND [server_principal_name]<>''sa'')
		OR [statement] LIKE ''%821ABE6A-06AB-4EA0-91AA-2C959E34B07B%'''

	EXEC sp_executesql @strSQL;

	/* CDR_Authorized */

	/* adding SQL Server service and SQL Server Agent service accounts */
	SET @sqlServiceAccounts = '';

	SELECT @sqlServiceAccounts = @sqlServiceAccounts +  N'session_server_principal_name =''' + service_account + N''' OR '
	FROM sys.dm_server_services
	GROUP BY service_account;

	SET @strSQL = N'use master; ALTER SERVER AUDIT [CDR_Authorized] WHERE session_server_principal_name <> ''$DIL_USER_ACCOUNT$'' -- Data Loading
		  AND ('

	SELECT @strSQL = @strSQL + '[session_server_principal_name] = ''' + UserName + ''' OR '
	FROM #server_principals

	SET @strSQL=CASE WHEN @isAddAccExists = 0 THEN @strSQL ELSE LEFT(@strSQL, LEN(@strSQL)-3) + ' OR ' END
	+ @sqlServiceAccounts +  
	+ ' [session_server_principal_name]=''$DATA_CAG_USER_ACCOUNT$'' -- Retrieve data for CAG
				OR [session_server_principal_name]=''$SECURITY_SERVICE_USER_ACCOUNT$'' -- Service
				OR [session_server_principal_name]=''$DATA_DAT_GROUP_ACCOUNT$'' -- User group for DAT 
				OR [session_server_principal_name]=''$DATA_PHA_READER_USER_ACCOUNT$'' -- PHA service account
				)
				OR [statement] LIKE ''%821ABE6A-06AB-4EA0-91AA-2C959E34B07B%'';'

	EXEC sp_executesql @strSQL

	-- swithch on the relevant audits
	IF @auditing_type <> @NO_AUDITING
		BEGIN
			EXEC ('USE master; ALTER SERVER AUDIT [CDR_Suspected] WITH (STATE = ON);');
		END
	IF @auditing_type=@SUSPICIOUS_AND_AUTHORIZED
		BEGIN
			EXEC ('USE master; ALTER SERVER AUDIT [CDR_Authorized] WITH (STATE = ON);');
		END

END
