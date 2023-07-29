from datetime import datetime, timezone
from dateutil.tz import tz


class RateLimit:
    def __init__(self):
        self.has_been_set = False
        self.limit = 0
        self.remaining = 0
        self.reset_date_time: datetime = datetime.now()

    def exceeded(self):
        # we do not know the current rate limit, so we can't check
        if not self.has_been_set:
            return False

        if self.remaining == 0:
            if self.time_until_reset() > 0:
                return True

        return False

    def cleared(self):
        self.has_been_set = False
        self.limit = 0
        self.remaining = 0
        self.reset_date_time = 0

    def set_rate_limit(self, limit, remaining, reset):
        self.has_been_set = True
        self.limit = limit
        self.remaining = remaining
        self.reset_date_time = reset

    def time_until_reset(self):
        if not self.has_been_set:
            return 0

        return (self.reset_date_time - datetime.now()).total_seconds()

    def update(self, headers):
        reset_date_time = datetime.strptime(
            headers["X-RateLimit-Reset"], '%Y-%m-%dT%H:%M:%S.%f%z'
        ).astimezone(tz=tz.tzlocal())
        reset_date_time = reset_date_time.replace(tzinfo=None)

        self.set_rate_limit(
            int(headers["X-RateLimit-Limit"]),
            int(headers["X-RateLimit-Remaining"]),
            reset_date_time
        )

    def __str__(self):
        return f'Limit: {self.limit}, Remaining: {self.remaining}, Reset: {self.reset_date_time}, Time until reset: {self.time_until_reset()}'


rate_limit = RateLimit()
