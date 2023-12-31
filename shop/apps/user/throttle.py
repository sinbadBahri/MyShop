from django.contrib.auth import get_user_model
from rest_framework.throttling import SimpleRateThrottle

from .helpers import verify_recaptcha

User = get_user_model()


class UserLoginRateThrottle(SimpleRateThrottle):
    scope = 'loginAttempts'

    def get_cache_key(self, request, view):
        user = User.objects.filter(email=request.data.get('email'))
        ident = user[0].pk if user else self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }

    def check_recaptcha(self, request, view):
        g_value = request.data.get('recaptcha')

        if g_value:
            is_verified = verify_recaptcha(g_value)
            return is_verified

        return False

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the throttle duration

        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        is_recaptcha_exists_and_verified = self.check_recaptcha(request, view)
        if len(self.history) >= self.num_requests and not is_recaptcha_exists_and_verified:
            return self.throttle_failure()

        return self.throttle_success()
