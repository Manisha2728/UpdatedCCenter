from django.db import models
from dbmconfigapp.models.base import ConfigurationEntityBaseModel, get_help_text
#from dbmconfigapp.models import SystemParameters
from django.core import validators
from configcenter.settings import get_param
#from django.db import connections, DEFAULT_DB_ALIAS

PAS_CHOICES_REMOTE = (
    (0, 'Apply local node policy'),
    (1, 'Opt In and Most updated consent'),
    (2, 'Opt Out and Most updated consent'),
    (3, 'Opt In and Most restricted consent'),
    (4, 'Opt Out and Most restricted consent'),
    )
      
# Create your models here.
class Node(ConfigurationEntityBaseModel):
    id                  = models.PositiveIntegerField(primary_key=True, unique=True)
    # This field, uid, was created in 16.2 to provide a user maintained node id field. It is split in the migrations in order to support
    #  upgrade with the table already populated with more than 1 row. in which case creating a unique field is not possible.
    # The migration (0004) creates the field with no contraints.
    # Then (0005) populate it with the value in id
    # Then we alter the field to this final state (unique, not null)
    uid                 = models.PositiveIntegerField(verbose_name='Id', null=False, unique=True, help_text= get_help_text('Defines the Node ID as an integer.<br>The Node ID must be unique in the federation.', ''))
    name                = models.CharField(verbose_name='Name',max_length=100, unique=True, help_text= get_help_text('Defines the Node Name as text.<br>It must be unique in the federation.', ''))
    application_server  = models.CharField(verbose_name='Application Server', unique=True, max_length=100 , help_text= get_help_text('The name of the application server, which is the NLB.<br>It must be unique in the federation.', ''))
    ppol_provider_node  = models.ForeignKey("self", on_delete=models.SET_NULL, verbose_name='PPOL Provider Node', blank=True, null=True, default=1, help_text=get_help_text('Defines the node that provides the Provider Registry Service (PPOL).<br>It is recommended to configure an identical value for the PPOL service on each node in order to configure one single centralized PPOL service in the federation.<br>Important! If a different PPOL service is configured on each node, the clustering of Patient and Provider data cannot be achieved between the PPOL instances.<br>For example, in Collaborate events will be displayed only for those Patients or Providers that are managed within the relevant PPOL Instance.<br>The rest will be filtered out by the Data Event Monitor. Additionally, Population Health will calculate rules (for Disease Populations) only for the patient indexes in the relevant PPOL Instance, and based only on the partial clinical data that is available.', ''))
    pas_option_remote   = models.IntegerField(verbose_name='Filter Federated Patient Records Policy', choices=PAS_CHOICES_REMOTE, default=0, help_text=get_help_text('This configuration is used to define the behavior of the Patient Consent functionality in a federated system where different nodes are configured with different Patient Consent policies (PAR).<br/>This configuration is required in order to enable each HIE participant to define and enforce its own Privacy and Consent requirements. The configuration enables each dbMotion node to define how to handle patient consent defined by other dbMotion nodes.<br/>In a federated system, a Patient Consent conflict might occur when the Patient Search returns patient indexes from different nodes (different systems) where each node has a different Patient Consent policy. The conflict is resolved by using this configuration to filter out of the Patient Search results all indexes that do not provide consent according to the consent policy of the specific node.<br/>The following guidelines apply to this configuration:<br/>- If all nodes in the federation have the same Patient Consent policy, there is no need to perform this configuration.<br/>- If different nodes have different Patient Consent policies it is mandatory to perform this configuration. If the configuration was not performed, the system uses the local Patient Consent policy definitions for all nodes.<br/>- The local node configuration applies only when exported to other nodes. The configuration for the actual local node behavior is located in: Security -> General Definition -> Defining Patient Consent Policy.', 'Apply local node policy'))
    request_from        = models.ForeignKey('Group', on_delete=models.SET_DEFAULT, related_name='request_from', verbose_name='Retrieve from', default=-1, help_text= get_help_text('Defines the Group of nodes to which this node can send requests and receive responses with data.<br>Possible values: All, None, Defined Group.<br><b>All:</b> Requesting information is applicable to all nodes including future added members. However, this might be limited by nodes that restrict the exchange of information with specified Groups.<br><b>None:</b> Requesting information outside this local node is disabled.<br><b>Defined Group:</b> Requesting information is applicable only to this Defined Group of nodes.<br>To define a Group of nodes, click the + sign to open the Federation Group window. Only one Group can be defined. To edit the Group settings, click the pencil sign.<br>When adding or changing a Group, the change applies to all configurations that refer to this Group.', 'None'))
    response_to         = models.ForeignKey('Group', on_delete=models.SET_DEFAULT, related_name='response_to', verbose_name='Provide to', default=-1, help_text= get_help_text('Defines the Group of nodes from which this node can accept requests and provide responses with data.<br>Possible values: All, None, Defined Group.<br><b>All:</b> Providing information is applicable to all nodes including future added members. However, this might be limited by nodes that restrict the exchange of information with specified Groups.<br><b>None:</b> Providing information outside this local node is disabled. However, if a node is set to not provide data, local data is always provided to local users.<br><b>Defined Group:</b> Providing information is applicable only to this Defined Group of nodes.<br>To define a Group of nodes, click the + sign to open the Federation Group window. Only one Group can be defined. To edit the Group settings, click the pencil sign.<br>When adding or changing a Group, the change applies to all configurations that refer to this Group.', 'None'))
    pl_active = models.BooleanField(verbose_name='Provide to Patient List', default=False, help_text=get_help_text('Determines whether this node provides data for the Patient List.', 'False.'))  
    node_confidentiality_level = models.CharField(verbose_name='Configuring Confidentiality Codes for Display of Node Outage Indication', max_length=200, help_text=get_help_text("This configuration (in Code^Code format) defines the user's confidentiality code(s) assigned to the user's Security Role, that determine whether this node's outage status is displayed in the dbMotion applications (with the red semaphore icon in the Retrieval Status table) when the node is in outage mode.<br>&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;If confidentiality code(s) are not defined here, the status of this node in outage mode will be displayed with the red semaphore icon.<br>&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;If the confidentiality code(s) defined here (for example, PSY code) were assigned to the user's Security Role, when this node is in outage mode the node will be displayed in the Retrieval Status table with the red semaphore icon.<br>&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;If the confidentiality code(s) defined here (for example, PSY code) were NOT assigned to the user's Security Role, when this node is in outage mode the node will NOT be displayed in the Retrieval Status table.<br>The confidentiality codes configured here must be configured in allowConfidentialityLevels configuration in the Security Management role profile.<br><br><em><u>Note:</u>&nbsp; This configuration is supported only in Israeli projects (that are implemented with the CDR Adapter).</em>", "Empty"), default="", blank=True)       
    is_available_during_document_search = models.BooleanField(verbose_name='Available for federated Document Search', default=False, help_text=get_help_text('If enabled, the node can be searched and can search other Elasticsearch nodes in the federation.<br/>If disabled, the node cannot be searched or searched by other Elasticsearch nodes in the federation.<br/><b>Note:</b> Restart services \"Communication Data Service\" and all its dependences to apply changes.', 'False.'))  
     
    def others(self):
        return Node.objects.exclude(pk=self.pk)

    def is_local(self):
        ####################
        # Important!!!
        # If the following code is changed, make sure to change the [federation_nodes_view] view.
        # Because the same calculation is done in the SQL side.
        ####################
        try:
            print("Computing is_local...")
            app_server = str(self.application_server).lower()
            print("app_server: '%s'" % app_server)
            
            ### 17.1 CU1 PR6 (http://dbm-jira:8080/browse/ST-3086, tbener, Feb 25, 2018) 
            # to support FQDN format in application_server field we need to cut it out before calculating the local node.
            domain_name = get_param('default_domain_name')
            print("Checking fqdn format. Domain name: '%s'" % domain_name)
            if domain_name:
                # if application_server is "app_name.server.com" we need tp check only the app_name part.
                if app_server.endswith(domain_name.lower()):
                    print("{app} ends with {dom}. Trimming...".format(app=app_server, dom=domain_name))
                    app_server = app_server[:-(len(domain_name)+1)]
            if not app_server:  # in case someone put only the domain name we'll result in an empty app_server.
                return False
            ###
            
            param_app_server_alias = get_param('application_server_alias','').lower()
            param_app_server = get_param('application_server','').lower()

            return app_server in [param_app_server_alias, param_app_server]

        except:
            return False
        
    is_local.boolean = True
    
    def save(self, *args, **kwargs):
        if(self.id == None):
            self.id = Node.objects.latest('id').id + 1
        super(Node, self).save(*args, **kwargs)
    
    #def enabled(self):
    #   return self.request_from != -1 & self.response_to != -1    

#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         if self.is_local():
#             self.enabled = True
#         ConfigurationEntityBaseModel.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        
    #===========================================================================
    # def has_constraints(self):
    #     connection = connections[DEFAULT_DB_ALIAS]
    #     con = connection
    #     cur = con.cursor()
    #     cur.cursor.callproc('fed_CheckNodeConstraints', [int(self.id)])
    #     answer = cur.cursor.fetchall()
    #     
    #     return answer[0][1]
    #===========================================================================
        

    def can_delete(self):
        # This method will not prevent the actual deleting, unless used explicitly, as in the admin
        # The reason is not to interfere Import
        msg = None
        if self.is_local():
            msg = 'is a local node'
        #elif self.node_set.exclude(pk=self.pk):
            #msg = 'is a PPOL provider node'
        #elif self.authoritysystems_set.exists():
            #msg = 'has related Authority System(s)'
        #elif self.dbmotionsystem_set.exists():
            #msg = 'has related Internal System(s)'
            
        if msg:
            return False, '%s %s and cannot be deleted.' % (self.name, msg)
        
        return True, ''

        
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "federation"
        verbose_name = 'Federation Node'
        history_meta_label = verbose_name
        help_text = """
        dbMotion supports the capability to connect multiple dbMotion instances (Nodes) that natively integrate with one another.<br>
        The connectivity of multiple Nodes is referred to as the Federation Solution. To implement a Federated Solution, perform the following configurations for all nodes on a single local node. Then export the Federation JSON file and import it to all the other nodes in the federation. After importing the JSON file or changing the node definitions click Apply. No service restart is required.<br>
        The Export and Import process assures alignment of all configurations between all nodes in the federation. It is not recommended to configure this alignment manually on each node.<br><br>
        
        The system identifies the local node and configures it as isLocal (true) automatically by recognizing the local application server name. The isLocal setting cannot be manually configured. Additionally, after each of the nodes import the JSON files, the isLocal (true) configuration is set automatically for the local node.<br><br> 
        
        To add a node, click Add Federation Node and follow the instructions.<br> 
        To delete a node, select the required row and click Action -> Delete. Then click Go.<br>
        To change a node configuration, click on the node name or ID and edit the node properties as required.<br><br>
        
        <b>Symmetric Topology</b> (where all nodes use identical federation settings) is highly recommended. In some cases, a single member might change the federation configurations locally, apply and test the changes prior to sharing the settings with all other nodes. During the test, the network is <b>asymmetric</b> and the configurations are applied differentially at each node.
        """
    
class Group(ConfigurationEntityBaseModel):  
    id             = models.IntegerField(verbose_name='Id', primary_key=True, unique=True, validators=[validators.MinValueValidator(1),], help_text= get_help_text('Defines the Group ID as an integer.<br>The Group ID must be unique in the federation.', '')) 
    name           = models.CharField(verbose_name='Name',max_length=100, unique=True, help_text= get_help_text('Defines a unique Group Name.', ''))
    node           = models.ManyToManyField('Node', verbose_name='Nodes', blank=True, null=True, help_text= get_help_text('Defines the nodes included in the Federation Group. Select the nodes from the dropdown menu.<br>Possible values: A Group can contain all nodes, specified nodes, or no nodes. Different Groups can have overlapping members.<br><br><b>To Delete a Group:</b> Because of references to the Group in various configurations, it is recommended to change the Group Name to Deleted and remove all group members. The Group remains available in the dropdown menu and can be referenced again and updated in the future. The behavior of an empty group is similar to a group with no (None) members.', ''))
    
    def __unicode__(self):
        return self.name
           
    class Meta:
        app_label = "federation"
        verbose_name = 'Federation Group'
        history_meta_label = verbose_name

    def save(self, *args, **kwargs):
        if(self.id == None):
            self.id = Group.objects.latest('id').id + 1
        super(Group, self).save(*args, **kwargs)
    
