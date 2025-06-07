import flask_login
import werkzeug.security as tools

class Usuario(flask_login.UserMixin):
    def __init__(self, email, password, username):
        self.__email = email
        self.__password = tools.generate_password_hash(password)
        self.__username = username
        self.logable = True  # Indicates if the user can log in

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.__email = email
    
    @property
    def username(self):
        return self.__username

    
    def check_password(self, password):
        return tools.check_password_hash(self.__password, password) and self.logable
    
    def set_password(self, password):
        self.__password = tools.generate_password_hash(password)

    @property
    def id(self):
        return self.__username
    
    def delete(self):
        self.__email = "user@delet.ed"
        self.logable = False
        flask_login.logout_user()
        

    @staticmethod
    def current_user():
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            return None
        return usr
    
    @staticmethod
    def find(srp, username):
       print("Finding user by username:", username)
       if srp.find_first(Usuario, lambda x: x.id == username):
           print("User found")
           return srp.find_first(Usuario, lambda x: x.id == username)
       else:
           print("User not found")
           return None
