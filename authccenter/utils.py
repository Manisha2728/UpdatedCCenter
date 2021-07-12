from django.contrib.auth.models import User
from authccenter.models.user import CCenterUser

FAKE_DJANGO_USER_NAME = 'ADUser_5CF4E2EB6974769EE2878EA'

def get_fake_django_user():
    try:
        user = User.objects.get(username = FAKE_DJANGO_USER_NAME)
        return user
    except:
        return None

def get_request_user_ids(request):
    user_id = 1    
    ccenter_user_id = None

    if(request != None and request.user != None):
        if(isinstance(request.user, CCenterUser)):
            fake_user = get_fake_django_user()
            if(fake_user != None):
                user_id = fake_user.pk
            ccenter_user_id = request.user.pk
        else:
            user_id = request.user.pk
        
    return user_id, ccenter_user_id

def get_user_to_dispay(obj):
    if(obj.ccenter_user != None):
        return obj.ccenter_user
    return obj.user

def get_user_name(obj):
    user = get_user_to_dispay(obj)
    if(user == None):
        return ''
    return user.get_full_name()

