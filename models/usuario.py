import flask_login

class Usuario(flask_login.UserMixin):
    def __init__(self, email, password):
        self.__email = email
        self.__password = password
    
    @property
    def email(self):
        return self.__email
    
    def ID(self):
        return self.__email
    
    def check_password(self, password):
        return self.__password == password
    
    