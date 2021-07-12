'''
Created on Jan 19, 2014

@author: EBliacher
'''

def createClinicalDomain(creator, primary_key,
                             page_help_text, 
                             page_name, 
                             tree_id, 
                             help_text_1, 
                             help_text_2, 
                             help_text_3, 
                             clinical_view_name, 
                             services, components, report_name = ""):
    page = creator
    page.page_help_text = page_help_text
    page.page_name = page_name
    page.tree_id = tree_id
    page.help_text_1 = help_text_1
    page.help_text_2 = help_text_2
    page.help_text_3 = help_text_3
    page.clinical_view_name = clinical_view_name
    page.report_name = report_name
    page.pk = primary_key
    page.save()
    page.services = services
    page.components = components
    return page;


def createPage(pageCreator, page_name, page_help_text, tree_id, services, components):
    # page_name is obsolete. See CCenter documentation (http://dbm-wiki/index.php?title=How_to_add_new_page#Create_empty_migration)

    page = pageCreator
    page.pk = 1
    page.page_name = page_name
    page.page_help_text = page_help_text
    page.tree_id = tree_id
    page.save()
    page.services = services
    page.components = components
    return page

def get_components_by_name(apps, names_list):
    components = []
    Components = apps.get_model("dbmconfigapp", "Component").objects

    for comp_name in names_list:
        components.append(Components.filter(name=comp_name)[0])

    return components

def createDataElement(creator, pk, clinical_domain, 
                      name, page_width, default_width, order, clinical_view_name, grid_name, 
                      enable=True,
                      report_width=None, default_report_width=None, report_field_name="", report_name="", 
                      hide_uom=0, concatenate_values=0, pl_parent=None, pv_parent_patient_display=None
                      ):
    dataElement = creator
    dataElement.pk = pk
    dataElement.name = name
    dataElement.page_width =page_width
    dataElement.default_width = default_width
    dataElement.enable = enable
    dataElement.report_width = report_width
    dataElement.default_report_width = default_report_width
    dataElement.order = order
    dataElement.clinical_view_name = clinical_view_name
    dataElement.clinical_domain = clinical_domain
    dataElement.grid_name = grid_name
    dataElement.report_name = report_name
    dataElement.report_field_name = report_field_name
    dataElement.hide_uom = hide_uom
    dataElement.concatenate_values = concatenate_values
    dataElement.pl_parent = pl_parent
    dataElement.pv_parent_patient_display = pv_parent_patient_display
    dataElement.save()
    return dataElement


    
    