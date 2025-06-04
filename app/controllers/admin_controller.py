class AdminController:
    def __init__(self, user_interface, current_user):
        self.user_interface = user_interface
        self.current_user = current_user
    
    def get_all_users(self):
        return self.user_interface.get_all_users()