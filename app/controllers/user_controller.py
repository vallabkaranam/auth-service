class UserController:
    def __init__(self, user_interface, current_user):
        self.user_interface = user_interface
        self.current_user = current_user
    
    def get_current_user(self):
        return self.current_user
