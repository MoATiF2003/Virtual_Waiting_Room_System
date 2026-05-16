from models.session_manager import SessionManager
from models.waiting_queue import WaitingQueue
from models.user import User
import time
import threading
import math

class Gateway:
    
    def __init__(self, max_capacity = 10, admit_rate = 2, session_timeout = 5):
        self.max_capacity = max_capacity
        self.admit_rate = admit_rate
        self.session_timeout = session_timeout
        self.session_manager = SessionManager(max_capacity = self.max_capacity)
        self.waiting_queue = WaitingQueue()
        self.all_users = {}

    def request_access(self, user_id):
        user = User(user_id = user_id, session_timeout = self.session_timeout)
        self.all_users[user_id] = user 

        if self.session_manager.has_capacity():
            self.session_manager.add_user(user)
        
            return {
                "status" : "ADMITTED",
                "message" : f"{user.user_id} entered website",
                "user" : user 
            }
        
        else:
            self.waiting_queue.add_user(user)
            
            return {
                "status" : "QUEUED",
                "message" : f"{user.user_id} added to waiting queue",
                "position" : self.waiting_queue.get_position(user.user_id),
                "user" : user
            }
    
    def process_queue(self):
        expired_users = self.session_manager.remove_expired_users()
        admitted_users = []
        admitted_count = 0

        while (
            self.session_manager.has_capacity() 
            and 
            not self.waiting_queue.is_empty()
            and
            admitted_count < self.admit_rate
        ):
            user = self.waiting_queue.admit_user()
            self.session_manager.add_user(user)
            admitted_users.append(user)
            admitted_count += 1

        return {
            "expired_users" : expired_users,
            "admitted_users" : admitted_users
        }
    
    def start_auto_processing(self, interval = 30):
        def auto_process():
            while True:
                result = self.process_queue()

                for user in result["expired_users"]:
                    print(f"EXPIRED: {user}")

                for user in result["admitted_users"]:
                    print(f"ADMITTED FROM QUEUE: {user}")
                
                print(f"Current Status: {self.system_status()}")

                time.sleep(interval)
        
        processing_thread = threading.Thread(
            target=auto_process,
            daemon=True
        )

        processing_thread.start()

    def system_status(self):
        return {
            "active_users" : self.session_manager.active_user_count(),
            "queued_users" : self.waiting_queue.queue_size(),
            "available_slots" : (
                self.session_manager.max_capacity - 
                self.session_manager.active_user_count()
            )
        }
    
    def calculate_estimated_wait(self, position):
        if self.session_manager.active_user_count() == 0:
            return 0
        
        remaining_times = []

        for user in self.session_manager.get_active_users():
            remaining_times.append(user.get_remaining_time())

        earliest_expiry = min(remaining_times)

        # batch_index = math.ceil(
        #     (position - 1) / self.admit_rate
        # )
        batch_index = (position - 1) // self.admit_rate

        additional_delay = batch_index * 60

        return earliest_expiry + additional_delay
    
    def get_user_status(self, user_id):
        if user_id not in self.all_users:
            return {
                "error" : "User not found"
            }
        
        user = self.all_users[user_id]

        if user.status == 'QUEUED':
            position = self.waiting_queue.get_position(user_id)
            # cycle_needed = math.ceil(
            #     position/self.admit_rate
            # )
            # estimated_wait_time = cycle_needed * 60

            estimated_wait_time = self.calculate_estimated_wait(position)

            return {
                "user_id" : user.user_id,
                "status" : user.status,
                "queue_position" : position,
                "estimated_wait_seconds" : estimated_wait_time 
            }
        
        elif user.status == 'ACTIVE':
            return {
                "user_id" : user.user_id,
                "status" : user.status,
                "remaining_session_seconds" : user.get_remaining_time()
            }
        
        elif user.status == 'EXPIRED':
            return {
                "user_id" : user.user_id,
                "status" : user.status
            }

    def get_dashboard_data(self):
        active_users_data = []
        queued_users_data = []

        for user in self.session_manager.get_active_users():
            active_users_data.append({
                "user_id": user.user_id,
                "remaining_session_seconds": user.get_remaining_time()
            })


        for position, user in enumerate(
            self.waiting_queue.get_all_users(),
            start=1
        ):

            # cycles_needed = math.ceil(
            #     position / self.admit_rate
            # )

            # estimated_wait = cycles_needed * 60

            estimated_wait = self.calculate_estimated_wait(position)

            queued_users_data.append({
                "user_id": user.user_id,
                "queue_position": position,
                "estimated_wait_seconds":
                    estimated_wait
            })

        return {
            "system_status": {
                "active_users":
                    self.session_manager.active_user_count(),
                "queued_users":
                    self.waiting_queue.queue_size(),
                "available_slots":
                    self.session_manager.max_capacity -
                    self.session_manager.active_user_count()
            },
            "active_users_data":
                active_users_data,
            "queued_users_data":
                queued_users_data
        }
        