from locust import between, clients
from EComm_Project.CommonLib.LogModule import *
from EComm_Project.CommonLib.UtilHelper import UtilHelper
from locust.exception import StopUser
from EComm_Project.CommonLib.UserLoader import UserLoader
from EComm_Project.UserLib.AbstractUser import AbstractUser


# import xmlrpc.client

# need to be used if we want to load users uniquely from another machine or workers
# user_proxy = xmlrpc.client.ServerProxy('http://server-ip-address')


class RegisteredHttpUser(AbstractUser):
    wait_time = between(1, 2)
    abstract = True

    def verify_login_success(self, response, email):
        if response.status_code != 200 or 'Authentication failed.' in response.text:
            response.failure("Failed to login, user: " + email + " Status Code : " + str(response.status_code))
            raise StopUser()
        return True

    def on_start(self):
        # TODO: Fetch one user from user list and login, store cookie and user info
        # need to be used if we want to load users uniquely from another machine or workers
        # user_obj = user_proxy.get_user()
        user_obj = UserLoader.get_user()
        form_data = {'email': user_obj['username'], 'passwd': user_obj['password'],
                     'back': 'my-account', 'SubmitLogin': ''}

        with self.client.post("/index.php?controller=authentication", form_data, headers=UtilHelper.get_base_header(),
                              catch_response=True) as response:
            if self.verify_login_success(response, user_obj['username']):
                Logger.log_message("Login successful with user : " + user_obj['username'], LogType.INFO)
                super().set_email(user_obj['username'])
                super().set_cookie(response.cookies)

    def on_stop(self):
        # TODO: Logout user from server when load test ends
        pass
