import django.dispatch

login_failure = django.dispatch.Signal(providing_args=["username", "exception"])