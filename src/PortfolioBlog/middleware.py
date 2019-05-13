from datetime import datetime
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
import json
from django.core.serializers.json import DjangoJSONEncoder
import types


class SessionExpiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        last_login = request.session.get('last_login', None)
        print(request.session.get('last_login'))
        now = datetime.now()

        if type(last_login) is type(now):
            if (now - last_login).minute > 60:
                # Do logout / expire session
                # and then...
                return HttpResponseRedirect("login")

        if not request.is_ajax():
            # don't set this for ajax requests or else your
            # expired session checks will keep the session from
            # expiring :)
            request.session['last_login'] = json.dumps(now, cls=DjangoJSONEncoder)
