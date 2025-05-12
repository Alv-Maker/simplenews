import flask_login

class Usuario(flask_login.UserMixin):
    def __init__(self, email, password):
        self.__email = email
        self.__password = password

    @property
    def email(self):
        return self.__email

    
    def check_password(self, password):
        return self.__password == password

    @property
    def id(self):
        return self.__email

    @staticmethod
    def current_user():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            return None
        return usr
    
    @staticmethod
    def find(srp, email):
       print("Finding user by email:", email)
       if srp.find_first(Usuario, lambda x: x.id == email):
           print("User found")
           return srp.find_first(Usuario, lambda x: x.id == email)
       else:
           print("User not found")
           return None
