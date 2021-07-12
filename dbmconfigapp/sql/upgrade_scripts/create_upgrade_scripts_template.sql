USE [dbmCCenter]
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[spWriteStringToFile]') AND type in (N'P', N'PC'))
BEGIN
	EXEC dbo.sp_executesql @statement = N'CREATE PROCEDURE spWriteStringToFile
	 (
	@String Varchar(max), --8000 in SQL Server 2000
	@Path VARCHAR(8000),
	@Filename VARCHAR(8000)

	--
	)
	AS
	DECLARE  @objFileSystem int
			,@objTextStream int,
			@objErrorObject int,
			@strErrorMessage Varchar(1000),
			@Command varchar(8000),
			@hr int,
			@fileAndPath varchar(8000)

	set nocount on

	select @strErrorMessage=''opening the File System Object''
	EXECUTE @hr = sp_OACreate  ''Scripting.FileSystemObject'' , @objFileSystem OUT

	Select @FileAndPath=@path+''\''+@filename
	if @HR=0 Select @objErrorObject=@objFileSystem , @strErrorMessage=''Creating file "''+ @FileAndPath +''"''
	if @HR=0 execute @hr = sp_OAMethod   @objFileSystem   , ''CreateTextFile''
		, @objTextStream OUT, @FileAndPath,2,True

	if @HR=0 Select @objErrorObject=@objTextStream, 
		@strErrorMessage=''writing to the file "''+@FileAndPath+''"''
	if @HR=0 execute @hr = sp_OAMethod  @objTextStream, ''Write'', Null, @String

	if @HR=0 Select @objErrorObject=@objTextStream, @strErrorMessage=''closing the file "''+@FileAndPath+''"''
	if @HR=0 execute @hr = sp_OAMethod  @objTextStream, ''Close''

	if @hr<>0
		begin
		Declare 
			@Source varchar(255),
			@Description Varchar(255),
			@Helpfile Varchar(255),
			@HelpID int
	
		EXECUTE sp_OAGetErrorInfo  @objErrorObject, 
			@source output,@Description output,@Helpfile output,@HelpID output
		Select @strErrorMessage=''Error whilst ''
				+coalesce(@strErrorMessage,''doing something'')
				+'', ''+coalesce(@Description,'''')
		raiserror (@strErrorMessage,16,1)
		end
	EXECUTE  sp_OADestroy @objTextStream
	EXECUTE sp_OADestroy @objFileSystem'
END
GO
sp_configure 'show advanced options', 1; 
GO 
RECONFIGURE; 
GO 

sp_configure 'Ole Automation Procedures', 1;  
GO  
RECONFIGURE;

create table #TableFieldsMetadata (TableName varchar(1000), --COLLATE Latin1_General_CI_AS, 
FieldName varchar(1000), --COLLATE Latin1_General_CI_AS, 
DefaultValue varchar(1000), --COLLATE Latin1_General_CI_AS,
IsKey bit NULL)

----- INPUT DYNAMIC DATA HERE
$INSERT_TABLE_FIELDS_METADATA$

DECLARE @version decimal(10,3)

select @version=max(cast([version]as decimal(10,3))) from [dbo].[dbmconfigapp_migrationmanager]

  create table #Tables (ID INT IDENTITY (1,1) ,
				SchemaName varchar(1000),--COLLATE Latin1_General_CI_AS ,
				TableName varchar(1000) --COLLATE Latin1_General_CI_AS  
				)

-- Prepare metadata table for INSERT
  insert into #Tables (SchemaName , TableName)
  SELECT DISTINCT  schema_name(A.schema_id) , A.name  
FROM [sys].[tables]  A
inner join #TableFieldsMetadata D
on A.name = D.TableName
INNER JOIN sys.partitions B ON A.object_id = B.object_id  

WHERE A.type = 'U'
AND index_id < 2 -- 0:Heap, 1:Clustered		
AND B.rows > 0
and NOT EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata T
			   WHERE D.TableName = T.TableName
			   AND T.IsKey IS NOT NULL)

DECLARE   @schema NVARCHAR(max)   , 
          @table NVARCHAR(max)   ,
		  @a int = 1 ,
		  @Path as varchar(8000) = '$_NODE_SHARED_FOLDER$\Services\CCenter\Data'
		  -- @Path as varchar(1000) = 'c:\temp\CCenterData'

DECLARE @DirTree TABLE (subdirectory nvarchar(255), depth INT)
INSERT INTO @DirTree(subdirectory, depth)
EXEC master.sys.xp_dirtree @Path


-- Create the @DataPath directory
IF NOT EXISTS (SELECT 1 FROM @DirTree )
EXEC master.dbo.xp_create_subdir @Path

-- DELETE\INSERT
   declare @insert_fields varchar(max),
          @select        varchar(max)  ,
          @error         varchar(500),
          @query         varchar(max) ,
		  @BeforeInsert         nvarchar(max)  , 
		  @AfterInsert         nvarchar(max)  , 
		  @insert         nvarchar(max) , 
		  @update_fields   nvarchar(max) , 
		  @where_fields nvarchar(max)
		  
	declare @values table(description varchar(max));

    declare  @AddingFieds table( FieldName varchar(1000) , DefaultValue varchar(1000))
    DECLARE @FieldName varchar(1000), 
	        @DefaultValue varchar(1000) 

 WHILE exists(SELECT TOP(1) 1 FROM #Tables)
  BEGIN

      SELECT @schema  = SchemaName, 
			 @table = TableName ,
			 @select = NULL,
			 @insert_fields  = NULL, 
			 @query = '' , 
			 @BeforeInsert = '' , 
			 @AfterInsert = '' , 
			 @insert = ''
	 FROM #Tables
	 WHERE ID =  @a 

	 delete from   @values

						  -- Get columns
						  select @insert_fields = isnull(@insert_fields + ', ', '') +'['+ c.name + ']',
								 @select = case type_name(c.system_type_id)
											  when 'varchar' then isnull(@select + ' + '', '' + ', '') + ' isnull('''''''' + cast(REPLACE([' + c.name + '],CHAR(39),'+ CHAR(39)+CHAR(39) + CHAR(39)+CHAR(39)+ CHAR(39)+CHAR(39)+ ') as varchar(max)) + '''''''', ''null'')'
											  when 'nvarchar' then isnull(@select + ' + '', '' + ', '') + ' isnull('''''''' + cast(REPLACE([' + c.name + '],CHAR(39),'+ CHAR(39)+CHAR(39) + CHAR(39)+CHAR(39)+ CHAR(39)+CHAR(39)+ ') as varchar(max)) + '''''''', ''null'')'
											  when 'datetime' then isnull(@select + ' + '', '' + ', '') + ' isnull('''''''' + convert(varchar(1000), [' + c.name + '], 121) + '''''''', ''null'')'
											  else isnull(@select + ' + '', '' + ', '') + 'isnull('''''''' + cast([' + c.name + '] as varchar(max)) + '''''''', ''null'')'
											end
									
							from sys.columns c with(nolock)							
								 inner join sys.tables t with(nolock) on t.object_id = c.object_id
								 inner join sys.schemas s with(nolock) on s.schema_id = t.schema_id
						   where s.name =@schema
							 and t.name =@table
							 AND EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata D
							             where c.name = D.FieldName
										 AND D.TableName =  @table);


										  insert into @AddingFieds (FieldName , DefaultValue)
										  SELECT FieldName , DefaultValue
										  FROM #TableFieldsMetadata
										   WHERE TableName =  @table
										   AND DefaultValue IS NOT NULL
				                         
										
										   WHILE EXISTS(SELECT TOP(1) 1 FROM @AddingFieds)
											   BEGIN
												  SELECT TOP(1) @FieldName  = FieldName, 
														        @DefaultValue = DefaultValue
												  FROM @AddingFieds
												
												  ---- new field
												  IF  CHARINDEX('['+@FieldName+']'  , @insert_fields)  = 0
												       BEGIN
															 SET @insert_fields = @insert_fields + ',' + @FieldName
															 SET @select = @select + '+'',''+''''''' + @DefaultValue +''''''''
                                                       END
												 
												  DELETE FROM @AddingFieds
												  WHERE FieldName  = @FieldName
												
											   END

						  set @insert_fields = '
	INSERT ' + @schema + '.' + @table + '(' + @insert_fields + ')';
						 
						  set @query = 'SELECT ' +  @select + ' FROM ' + @schema + '.' + @table + '  ' ;
						  
						  insert into @values(description)
						  exec(@query);


						  set @insert = isnull(@insert + char(10), '') + '--' + upper(@schema + '.' + @table);

						IF @table = 'via_authoritysystems'
						      BEGIN
								  select @insert = @insert + char(10) + 'IF NOT EXISTS(SELECT TOP(1) 1 FROM dbo.via_authoritysystems 
		WHERE CHARINDEX(''|''+[source_system_dbMotion_oid] +''|'' ,'''+ REPLACE(v.description ,CHAR(39),'|')+''') > 0) ' + @insert_fields  + char(10) + 'values(' + v.description + ');' + char(10)  + char(10)
								  from @values v
								  where isnull(v.description, '') <> '';
															 
							  END
						ELSE IF @table = 'dbmconfigapp_agentpphostedapp'
						      BEGIN 
								  DECLARE @insert1 varchar(max)
								  set  @insert1 = ''
								  select @insert1 = @insert1 + 
'
IF NOT EXISTS(SELECT TOP(1) 1 FROM dbo.dbmconfigapp_agentpphostedapp 
		WHERE CHARINDEX(''|''+[app_name] +''|'' ,'''+ REPLACE(v.description ,CHAR(39),'|')+''') > 0) ' + @insert_fields  + char(10) + 'values(' + v.description + ');' + char(10)  + char(10)
								  from @values v
								  where isnull(v.description, '') <> ''
								  and CHARINDEX('Care Coordination' , v.description) = 0
								  and CHARINDEX('Clinical View Agent' , v.description) = 0;

								  IF isnull(@insert1, '') = ''
									BEGIN
									 DELETE FROM #Tables
									 WHERE ID =  @a 
									 SET @a = @a + 1

									 CONTINUE
									END
									
								 select @insert = @insert + @insert1
							  END
						ELSE
						  BEGIN
							  select @insert = @insert + char(10) + @insert_fields + char(10) + 'VALUES(' + v.description + ');' + char(10)  + char(10)
							  from @values v
							  where isnull(v.description, '') <> '';
						  END 

						IF @table = 'dbmconfigapp_ehragentmeasurementproperties' AND @version < 19.6
							SET @AfterInsert = @AfterInsert + '
UPDATE dbmconfigapp_ehragentmeasurementproperties SET [hide_uom] = 1 WHERE [domain_id] IN (''HeartRate'',''BloodPressure'')
							'
						SET @BeforeInsert = ' USE dbmCCenter
GO
IF OBJECT_ID('''+upper(@schema + '.' + @table) + ''') IS NOT NULL
			BEGIN 
			BEGIN TRAN 
			'
						IF @table != 'dbmconfigapp_agentpphostedapp'
						BEGIN
							SET @BeforeInsert = @BeforeInsert + '
			DELETE ' +upper(@schema + '.' + @table)

							IF OBJECTPROPERTY(OBJECT_ID(@schema + '.' + @table), 'TableHasIdentity') = 1			
								  BEGIN
							 
									  SET @BeforeInsert = @BeforeInsert + ' SET IDENTITY_INSERT '+upper(@schema + '.' + @table) +' ON ' 
									  SET @AfterInsert = @AfterInsert + ' SET IDENTITY_INSERT '+upper(@schema + '.' + @table) +' OFF '
								
								  END
						END
					
						set @insert = @BeforeInsert + @insert  + @AfterInsert + ' COMMIT END'
						set @table = @table + '_ins.sql'
						exec spWriteStringToFile  @String  = @insert, --8000 in SQL Server 2000
						@Path  = @Path,
						@Filename  = @table

			 DELETE FROM #Tables
			 WHERE ID =  @a 
			 SET @a = @a + 1
	END


---- UPDATE
 TRUNCATE TABLE #Tables
 SET @a = 1 
 insert into #Tables (SchemaName , TableName)
  SELECT DISTINCT schema_name(A.schema_id) , A.name  
FROM [sys].[tables]  A
inner join #TableFieldsMetadata D
on A.name = D.TableName
INNER JOIN sys.partitions B ON A.object_id = B.object_id  

WHERE A.type = 'U'
AND index_id < 2 -- 0:Heap, 1:Clustered		
AND B.rows > 0
and  EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata T
			   WHERE D.TableName = T.TableName
			   AND T.IsKey IS NOT NULL)

WHILE exists(SELECT TOP(1) 1 FROM #Tables)
  BEGIN
    
      SELECT @schema  = SchemaName, 
			 @table = TableName ,
			 @select = NULL,
			 @insert_fields  = NULL, 
			 @query = '' , 
			 @BeforeInsert = '' , 
			 @AfterInsert = '' , 
			 @insert = '' , 
			 @update_fields = NULL ,
			 @where_fields = NULL 
	 FROM #Tables
	 WHERE ID =  @a 

	 IF (@table='dbmconfigapp_clinicalcodedisplay' AND NOT EXISTS 
		(select [display_as] from [dbo].[dbmconfigapp_clinicalcodedisplay] 
			where display_as like '%Preferred%' and display_as like '%Baseline%' and display_as like '%Local%' and display_as like '%Text%'))
	 BEGIN
		DELETE FROM #Tables
		WHERE ID =  @a 
		SET @a = @a + 1
		CONTINUE
	 END

	 delete from   @values
	 ---
	   select @update_fields = isnull(@update_fields + ' +'','' +'' ', '') +' ['+ c.name + '] = ''' +
								case type_name(c.system_type_id)
											  when 'varchar' then isnull(@select + ' + '', '' + ', '') + '+ isnull('''''''' + cast(REPLACE([' + c.name + '],CHAR(39)'+ CHAR(39)+CHAR(39) + CHAR(39)+CHAR(39)+ CHAR(39)+CHAR(39)+ ') as varchar(max)) + '''''''', ''null'')'
											  when 'nvarchar' then isnull(@select + ' + '', '' + ', '') + '+ isnull('''''''' + cast(REPLACE([' + c.name + '],CHAR(39),'+ CHAR(39)+CHAR(39) + CHAR(39)+CHAR(39)+ CHAR(39)+CHAR(39)+ ') as varchar(max)) + '''''''', ''null'')'
											  when 'datetime' then isnull(@select + ' + '', '' + ', '') + '+ isnull('''''''' + convert(varchar(1000), [' + c.name + '], 121) + '''''''', ''null'')'
											  else isnull(@select + ' + '', '' + ', '') + ' + isnull('''''''' + cast([' + c.name + '] as varchar(max)) + '''''''', ''null'')'
											end + ''
		
		from sys.columns c with(nolock)							
				inner join sys.tables t with(nolock) on t.object_id = c.object_id
				inner join sys.schemas s with(nolock) on s.schema_id = t.schema_id
		where s.name =@schema
			and t.name =@table 
			AND c.is_identity = 0 ---???
			AND EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata D
						where c.name = D.FieldName
						AND D.TableName =  @table
						AND D.IsKey IS NULL);
--select '00',@a as a , @update_fields
	    select @where_fields = isnull(@where_fields + '+'' AND ', '') +' ['+ c.name + '] =''' + ---cast([' + c.name + ']  as varchar(1000))'
											
							  case type_name(c.system_type_id)
							                  when 'varchar' then  isnull(@select + ' + '', '' + ', '') + ''''' +  cast([' + c.name + '] as varchar(max)) + '''''''
											  when 'nvarchar' then  isnull(@select + ' + '', '' + ', '') + ''''' +  cast([' + c.name + '] as varchar(max)) + '''''''
											  when 'datetime' then  isnull(@select + ' + '', '' + ', '') + ''''' +  cast([' + c.name + '] as varchar(1000)) + '''''''
											  else isnull(@select + ' + '', '' + ', '') + ' +  cast([' + c.name + '] as varchar(max)) ''' 
											end + ' '''
									
		from sys.columns c with(nolock)							
				inner join sys.tables t with(nolock) on t.object_id = c.object_id
				inner join sys.schemas s with(nolock) on s.schema_id = t.schema_id
		where s.name =@schema
			and t.name =@table
			AND EXISTS(SELECT TOP(1) 1 FROM #TableFieldsMetadata D
						where c.name = D.FieldName
						AND D.TableName =  @table
						AND D.IsKey IS NOT NULL);
	--select '11',@a as a ,@where_fields  as '@where_fields' 

        SET @query =  'SELECT ' + ''' UPDATE ' + @schema + '.' + @table + '
		SET   '  + @update_fields + '
		'+ ' + '' 
		WHERE ' + @where_fields		
		+ ' from ' + @schema + '.' + @table + '  ' ;
		
--select '22',@a as a , @update_fields,@where_fields  as '@where_fields' ,@query


						  insert into @values(description)
						  exec(@query);


--select '33' , * from @values
						  set @insert = isnull(@insert + char(10), '') + '--' + upper(@schema + '.' + @table);
							--select @insert as '00'
						  select @insert = @insert + char(10) +   v.description + ';' + char(10)  + char(10)
						  from @values v
						  where isnull(v.description, '') <> '';

		SET @BeforeInsert = ' USE dbmCCenter
						
						IF OBJECT_ID('''+upper(@schema + '.' + @table) + ''') IS NOT NULL
									BEGIN '
						set @insert = @BeforeInsert + @insert  +  ' END'
	 ------
				set @table = @table + '_upd.sql'
---select '55' , @table , @BeforeInsert as '@BeforeInsert', @insert as '@insert'
				exec spWriteStringToFile  @String  = @insert, --8000 in SQL Server 2000
				@Path  = @Path,
				@Filename  = @table

		DELETE FROM #Tables
		WHERE ID =  @a 
		SET @a = @a + 1
	END

---table dbmCCenter.dbo.dbmconfigapp_dbfiles 

   SELECT  @insert ='' ,  @query = '' 
   delete from   @values

set @table = 'dbmconfigapp_dbfiles_ins.sql'


 select @query = 
 'select ' + 
 ''' 
	IF NOT EXISTS(SELECT TOP(1) 1 FROM dbo.dbmconfigapp_dbfiles T WHERE T.[filename] ='''''' + [filename] + '''''')
		INSERT INTO dbo.dbmconfigapp_dbfiles ( [filename], [data], [size]) ''' +
  '+'' 
		SELECT '' +''''' + ''''' + [filename] +''''''''+ '''+ ', '+''' +''''''''+ 
  cast([data] as nvarchar(max)) +''''''''+ '''+ ', '+''' +''''''''+ cast([size] as varchar(1000))+ ''''''
  '''
  + ' FROM dbo.dbmconfigapp_dbfiles '

--	select @query
						  insert into @values(description)
						  exec(@query);
	
						  select @insert = @insert + char(10)  + v.description  + char(10)  + char(10)
						  from @values v
    select @insert = 'USE dbmCCenter ' + @insert
	exec spWriteStringToFile  @String  = @insert, --8000 in SQL Server 2000
				@Path  = @Path,
				@Filename  = @table

drop table #TableFieldsMetadata
drop table #Tables

GO
EXEC sp_configure 'Ole Automation Procedures', 0;  
GO  
RECONFIGURE;
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[spWriteStringToFile]') AND type in (N'P', N'PC'))
DROP PROCEDURE dbo.spWriteStringToFile
GO
go
	


