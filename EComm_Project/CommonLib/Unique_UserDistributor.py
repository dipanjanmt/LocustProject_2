import csv
import os
import threading
from xmlrpc.server import SimpleXMLRPCServer


class UserDistributor:
    # user_list will contain all the users credentials from user.csv file
    user_list = []
    csv_file_path = os.getcwd() + "/Data/user.csv"
    USER_LOCK = threading.Lock()

    @staticmethod
    def load_users():
        reader = csv.DictReader(open(UserDistributor.csv_file_path))
        for line_elem in reader:
            UserDistributor.user_list.append(line_elem)

    @staticmethod
    def get_user():
        with UserDistributor.USER_LOCK:
            if len(UserDistributor.user_list) < 1:
                UserDistributor.load_users()
            user_obj = UserDistributor.user_list.pop()
            return user_obj


server = SimpleXMLRPCServer(("192.168.1.119", 8000))
UserDistributor.load_users()
print("\nUser Distributor Service Started ... Listening On Port 8000")
server.register_function(UserDistributor.get_user, "get_user")
server.serve_forever()
