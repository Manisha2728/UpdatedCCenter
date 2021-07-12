CREATE OR ALTER VIEW dbo.federation_nodes_view
AS

WITH    NodeNames
          AS ( SELECT   SP.param_value
               FROM     dbo.dbmconfigapp_systemparameters SP
               WHERE    SP.param_name IN ( '$_NODE_ALIAS_NAME$',
                                           '$_NODE_APP_SERVER$' )
             ),
        DomainName
          AS ( SELECT   SP.param_value
               FROM     dbo.dbmconfigapp_systemparameters SP
               WHERE    SP.param_name IN ( '$_NODE_ACCESS_ABSOLUTE_DOMAIN$' )
               UNION
               SELECT   ''
             )

SELECT DISTINCT 
		n.id,
        n.uid AS node_id,
        n.name,
        n.application_server,
        n.pas_option_remote,
        n.ppol_provider_node_id,
        n.request_from_id,
        n.response_to_id,
        n.pl_active,
        n.node_confidentiality_level,
		n.is_available_during_document_search,
        p.application_server AS ppol_provider_application_server,
        CAST(CASE WHEN AN.AppName IS NOT NULL 
				THEN 1
				ELSE 0
        END AS BIT) AS IsLocal,
        CAST(CASE WHEN n.request_from_id = -1
                       AND n.response_to_id = -1
                       AND AN.AppName IS NULL 
					THEN 0
					ELSE 1
             END AS BIT) AS enabled
FROM    dbo.federation_node n
LEFT JOIN dbo.federation_node p ON n.ppol_provider_node_id = p.id
LEFT JOIN ( SELECT DISTINCT REPLACE(NN.param_value, '_', '[_]') 
							+ CASE WHEN DN.param_value <> '' 
									THEN '_' + REPLACE(DN.param_value, '_', '[_]') 
									ELSE '' 
							END AS AppName
            FROM    NodeNames NN
            CROSS APPLY DomainName AS DN
          ) AS AN ON n.application_server LIKE AN.AppName
