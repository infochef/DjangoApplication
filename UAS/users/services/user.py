from abc import ABC, abstractmethod

class UserService(ABC):

    @abstractmethod
    def sign_up(self, user_id, login_id, password, role, email, first_name, last_name):
        pass

    @abstractmethod
    def user_login(self, login_id, password, role):
        pass

    @abstractmethod
    def user_logout(self):
        pass
    
    @abstractmethod
    def user_account_details(self,user_id, login_id, role, email, first_name, last_name):
        pass

    @abstractmethod
    def forgot_password(self, login_id, password, role):
        pass

    @abstractmethod
    def forgot_loginid(self, login_id, password, role):
        pass

    @abstractmethod
    def update_account_details(self, password, role, email, first_name, last_name):
        pass
    
    @abstractmethod
    def get_user_details(self, user_id):
        pass