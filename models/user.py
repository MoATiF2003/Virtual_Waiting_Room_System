from datetime import datetime, timedelta

class User:
    SESSION_DURATION = 5
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.join_time = None
        self.expiry_time = None
        self.status = 'CREATED'

    def start_session(self):
        self.join_time = datetime.now()
        self.expiry_time = (
            self.join_time +
            timedelta(minutes=self.SESSION_DURATION)
        )
        self.status = 'ACTIVE'

    def is_expired(self):
        if self.expiry_time is None:
            return False
        return datetime.now() >= self.expiry_time

    def get_remaining_time(self):
        if self.expiry_time is None:
            return 0
        remaining = self.expiry_time - datetime.now()
        return max(0, int(remaining.total_seconds()))
    
    def __str__(self):
        return f"{self.user_id} | Status: {self.status}"