CREATE OR ALTER PROCEDURE [dbo].[adm_GetTableValues]
		@tableName varchar(255) = ''
		
	AS
	SET NOCOUNT ON
	BEGIN
	
		DECLARE @COLUMN_NAME as nvarchar(128),
				@DATA_TYPE as nvarchar(128),
				@ORDINAL_POSITION nvarchar(2),
				@str nvarchar(max)
		
		set @tableName = parsename(@tableName,1)
				
	
		DECLARE db_cursor CURSOR FOR  
		SELECT COLUMN_NAME, DATA_TYPE, ORDINAL_POSITION
		FROM INFORMATION_SCHEMA.COLUMNS
		WHERE TABLE_NAME = @tableName
	
		OPEN db_cursor   
		FETCH NEXT FROM db_cursor INTO @COLUMN_NAME, @DATA_TYPE, @ORDINAL_POSITION
		
		WHILE @@FETCH_STATUS = 0   
		BEGIN   
			   SET @str = 'SELECT ''' + @tableName + ''', RowNumber = row_number() OVER (ORDER BY id), ''' + @COLUMN_NAME + ''', [' + @COLUMN_NAME + '], ''' + @DATA_TYPE + ''', ' + @ORDINAL_POSITION + ' FROM ' + @tableName
			   
			   INSERT INTO #Properties([tableName], [RowNumber], [name], [value], [type], [ORDINAL_POSITION])
			   EXEC (@str)		   
	
			   FETCH NEXT FROM db_cursor INTO @COLUMN_NAME, @DATA_TYPE, @ORDINAL_POSITION
		END   
		
		
	
		CLOSE db_cursor   
		DEALLOCATE db_cursor
		
	END

