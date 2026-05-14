class SessionManager:

    def __init__(self, max_capacity = 10):
        self.max_capacity = max_capacity
        self.active_users = []

    def has_capacity(self):
        return self.active_user_count() < self.max_capacity

    def add_user(self, user):
        user.start_session()
        self.active_users.append(user)
    
    def remove_expired_users(self):
        expired_users = []
          
        for user in self.active_users:
            if user.is_expired():
                user.status = 'EXPIRED'
                expired_users.append(user)

        for user in expired_users:
            self.active_users.remove(user)
        
        return expired_users

    def active_user_count(self):
        return len(self.active_users)

    def get_active_users(self):
        return self.active_users
