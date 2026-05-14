from collections import deque

class WaitingQueue:

    def __init__(self):
        self.queue = deque()

    def add_user(self, user):
        user.status = "QUEUED"
        self.queue.append(user)
    
    def admit_user(self):
        if self.is_empty():
            return None
        user = self.queue.popleft()
        user.status = 'ACTIVE'
        return user

    def get_position(self, user_id):    
        for i, user in enumerate(self.queue):
            if user.user_id == user_id:
                return i + 1
        return -1

    def is_empty(self):
        return len(self.queue) == 0
    
    def queue_size(self):
        return len(self.queue)
    
    def get_all_users(self):
        return list(self.queue)