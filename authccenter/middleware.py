from authccenter.models.user import CCenterUser
from django.contrib.sessions.models import Session
import logging
from authccenter.apps import log_success_action
from django.utils.deprecation import MiddlewareMixin

class ConcurentSessionMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        if isinstance(request.user, CCenterUser):
            stored_session_key = request.user.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session key, delete the stored_session_key
            # from the Session table
            if stored_session_key and stored_session_key != request.session.session_key:
                session = Session.objects.filter(session_key=stored_session_key).first()
                if(session):
                    session.delete()
                    log_success_action(request.user, 'Logout')
                    logger = logging.getLogger('django')
                    logger.warning("Concurrent CCenter session detected for user '%s'" % request.user.username)

            request.user.session_key = request.session.session_key
            request.user.save()

        return None
