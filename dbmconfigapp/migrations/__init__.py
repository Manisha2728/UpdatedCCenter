from django.contrib.contenttypes.models import ContentType

def noop(apps, schema_editor):
    return None


def remove_content_type(appName, modelName):
    content_type = ContentType.objects.filter(app_label=appName, model=modelName)
    print("Removing ContentType: {0} - {1}".format(appName, modelName))
    if content_type.exists():
        content_type.delete()
