from locust import between
from EComm_Project.CommonLib.UtilHelper import UtilHelper
from EComm_Project.CommonLib.LogModule import LogType, Logger
from EComm_Project.UserLib.AbstractUser import AbstractUser


class GuestHttpUser(AbstractUser):
    wait_time = between(1, 2)
    abstract = True

    def on_start(self):
        with self.client.get("/index.php", headers=UtilHelper.get_base_header(), catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Failed to navigate to home page with Guest user, STATUS CODE: "
                                 + str(response.status_code))
                Logger.log_message("Failed to navigate to home page with Guest user, STATUS CODE: " +
                                   " Status Code - " + str(response.status_code), LogType.ERROR)
            else:
                super().set_cookie(response.cookies)

    def on_stop(self):
        pass
