CREATE OR ALTER PROCEDURE [dbo].[security_CheckDomainConstraints]
		@domain_id int
		
AS
SET NOCOUNT ON
BEGIN
	

	IF EXISTS(SELECT top 1 1 from [dbmSecurity].[dbo].[Users] where [UserStorageID] = @domain_id)
	BEGIN
		SELECT  CanBeDeleted = 'False',
				[Message] = 'Involved in users bindings'
				
		RETURN
	END

	SELECT CanBeDeleted = 'True',
		   [Message] = 'can_delete'
	

END
