CREATE OR ALTER PROCEDURE [dbo].[fed_CheckNodeConstraints]
		@node_id int
		
AS
SET NOCOUNT ON
BEGIN
	

	IF EXISTS(SELECT top 1 1 from [dbmFederation].[dbo].[federation_ContractBindings] where [LocalNodeID] = @node_id OR [RemoteNodeID] = @node_id)
	BEGIN
		SELECT  CanBeDeleted = 'False',
				[Message] = 'involved in contract bindings'
				
		RETURN
	END

	IF EXISTS(SELECT top 1 1 from [dbmFederation].[dbo].[federation_LocalNodePolicies] where [LocalNodeID] = @node_id)
	BEGIN
		SELECT  CanBeDeleted = 'False',
				[Message] = 'has local node policies'
				
		RETURN
	END

	IF EXISTS(SELECT top 1 1 from [dbmFederation].[dbo].[federation_RemoteNodePolicies] where [LocalNodeID] = @node_id OR [RemoteNodeID] = @node_id)
	BEGIN
		SELECT  CanBeDeleted = 'False',
				[Message] = 'involved in remote node policies'
				
		RETURN
	END

	SELECT CanBeDeleted = 'True',
		   [Message] = 'can_delete'
	

END
