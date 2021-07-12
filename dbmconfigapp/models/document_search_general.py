import sys
from django.db import models
from dbmconfigapp.models.base import PageBaseModel, ConfigurationEntityBaseModel,\
    get_help_text
from django.core import validators

CONTENT_FREE_SYSTEMS_MODE = (
    (1, 'None'),
    (2, 'Custom'),
    (3, 'All')
    )

class DocumentSearchGeneral(PageBaseModel):
    
    def __unicode__(self):
        return self.page_name
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Document Search General"
        
class DocumentSearchGeneralProperties(ConfigurationEntityBaseModel):
    parent =                models.ForeignKey('DocumentSearchGeneral', on_delete=models.SET_NULL, null=True, default=1, editable=False)
    content_free_systems_mode   =        models.IntegerField(verbose_name='Search metadata only mode:', choices=CONTENT_FREE_SYSTEMS_MODE, default=1, help_text='Systems are configured to search content and metadata, or search metadata only. Systems configured for metadata search only do not index content into Elasticsearch, meaning content is not available for searching. This setting specifies which systems to search using metadata only.<br/><b>Note:</b> The setting affects the indexing process, but not the search process, and does not affect documents already indexed in Elasticsearch.<br/>* <b>None:</b> None of the systems are defined to support metadata search only. All systems support both metadata and content search for supported document types.<br/>* <b>Custom:</b>  Systems are defined by the organization to support metadata search only, using the document ID_Root of the clinical document. Use the pipe symbol [|] as a delimiter between systems.<br/>* <b>All:</b>  All systems are defined to support metadata search only.<br/><i>Default: None.</i>')
    content_free_systems    = models.TextField(verbose_name='Systems to CDR metadata search systems:', blank=True, default='', help_text=get_help_text('''
        Define source systems to metadata search only. Use the pipe symbol [|] as a delimiter between systems. Use the document Id_Root from clinicalDocument table.<br/><b>Note:</b> Changes to this setting does not affect past indexing.
    ''','Empty'))
    index_free_systems    = models.TextField(verbose_name='Systems to omit from index process:', blank=True, default='', help_text=get_help_text('''
        Define source systems to omit during indexing. Use the pipe symbol [|] as a delimiter between systems. Use the document Id_Root from clinicalDocument table.<br/><b>Note:</b> Changes to this setting does not affect past indexing.''','Empty'))
    is_ds_of_cdr_enabled = models.BooleanField(verbose_name='Enable indexing and searching for CDR clinical documents', default=False, help_text=get_help_text('To conduct a document search, the Elasticsearch engine must index the documents that are loaded in the CDR. In Patient View, this setting enables a document search field in the Documents category.<br/><b>Note:</b> Users must be assigned a security task to conduct a search.', 'False.<br/><br/><br/><br/>'))
    is_ds_of_external_enabled = models.BooleanField(verbose_name='Enable indexing and searching for External clinical documents', default=False, help_text=get_help_text('To conduct a document search, the Elasticsearch engine must index the documents that are loaded in the External documents repositories. In Patient View, this setting enables a document search field in the External Documents category.<br/><b>Note 1:</b> The search for external documents is supported only on metadata fields.<br/><b>Note 2:</b> Users must be assigned a security task to conduct a search.', 'False.<br/><br/><br/><br/>'))

    def __unicode__(self):
        return ''
    
    class Meta:
        app_label = "dbmconfigapp"
        verbose_name= "Document Search General"