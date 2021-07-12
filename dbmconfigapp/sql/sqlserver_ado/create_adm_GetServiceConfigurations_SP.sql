
	CREATE OR ALTER PROCEDURE [dbo].[adm_GetServiceConfigurations]
		@ServiceCodeName nvarchar(60) = ''
		
	AS
	DECLARE @ErrorMessage NVARCHAR(4000);
	DECLARE @ErrorSeverity INT;
	DECLARE @ErrorState INT;
		
	BEGIN TRY
		
		SET @ServiceCodeName = LTRIM(RTRIM(@ServiceCodeName))
				
		IF @ServiceCodeName = ''
		BEGIN
			SELECT 
				@ErrorMessage = 'No rows returned.',
				@ErrorSeverity = 16,
				@ErrorState = 1;
		
			-- Use RAISERROR inside the CATCH block to return error
			-- information about the original error that caused
			-- execution to jump to the CATCH block.
			RAISERROR (@ErrorMessage, -- Message text.
						@ErrorSeverity, -- Severity.
						@ErrorState -- State.
						);
		END
		
		DECLARE @modelName as nvarchar(60),
				@tableName as nvarchar(128)
			
				
		CREATE TABLE #Properties(
			[tableName] nvarchar(128),
			[RowNumber] int,
			[name] nvarchar(128),
			[type] nvarchar(128),
			[value] nvarchar(max),
			[ORDINAL_POSITION] int
		)
		
		DECLARE tables_cursor CURSOR FOR  
		SELECT distinct m.model_name
		FROM dbo.dbmconfigapp_service s
				inner join dbo.dbmconfigapp_modeldescriptor_services r
				on s.id = r.service_id
				inner join dbo.dbmconfigapp_modeldescriptor m
				on r.modeldescriptor_id = m.id
		WHERE s.code_name = @ServiceCodeName
		AND m.export_in_api = 1
		
				 
		
		OPEN tables_cursor   
		FETCH NEXT FROM tables_cursor INTO @tableName
		
		WHILE @@FETCH_STATUS = 0   
		BEGIN
				EXEC dbo.adm_GetTableValues  @tableName	     
		
				FETCH NEXT FROM tables_cursor INTO @tableName
		END   
		
		CLOSE tables_cursor   
		DEALLOCATE tables_cursor
			
		
		IF EXISTS(SELECT TOP(1) 1 FROM #Properties)
		BEGIN
			SELECT serviceName = @ServiceCodeName,
			(
				SELECT tableName as modelName, tableName,
				(
					SELECT 
					(
						SELECT [name], ISNULL([value], '') as [value], [type]
						FROM #Properties
						WHERE RowNumber = P.RowNumber 
								and tableName = P.tableName
						ORDER BY [ORDINAL_POSITION]
						FOR XML RAW('CCProperty'), TYPE
					)
					FROM #Properties P
					WHERE P.tableName = T.tableName
					GROUP BY P.tableName, P.RowNumber
					FOR XML RAW('CCRecord'), TYPE
				)
				FROM #Properties T
				GROUP BY tableName
				ORDER BY tableName
				FOR XML RAW('CCModel'), TYPE
			)
			FOR XML RAW('CCResponse'), TYPE
		END
		ELSE 
			SELECT 
				@ErrorMessage = 'No rows returned.',
				@ErrorSeverity = 16,
				@ErrorState = 1;
		
			-- Use RAISERROR inside the CATCH block to return error
			-- information about the original error that caused
			-- execution to jump to the CATCH block.
			RAISERROR (@ErrorMessage, -- Message text.
						@ErrorSeverity, -- Severity.
						@ErrorState -- State.
						);
			
	END TRY
		
	BEGIN CATCH
		
		SELECT 
		    @ErrorMessage = ERROR_MESSAGE(),
		    @ErrorSeverity = ERROR_SEVERITY(),
		    @ErrorState = ERROR_STATE();
		
		-- Use RAISERROR inside the CATCH block to return error
		-- information about the original error that caused
		-- execution to jump to the CATCH block.
		RAISERROR (@ErrorMessage, -- Message text.
		            @ErrorSeverity, -- Severity.
		            @ErrorState -- State.
		            );
	END CATCH