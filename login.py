import pickle
import os

file = open(r"user_dir.dat", "ab+")
file.close()


def register_new():
    username = input("Enter username: ")
    user_dir = open(r"user_dir.dat", "rb+")
    try:
        while True:
            readinfo = pickle.load(user_dir)
            if os.path.getsize(r"user_dir.dat") == 0:
                user_dir.close()
                user_dir = open(r"user_dir.dat", "ab+")
                pwd = input("Enter your password: ")
                pwd_ch = input("Re-enter your password: ")
                while True:
                    if pwd == pwd_ch:
                        userdict = {}
                        userdict["username"] = username
                        userdict["password"] = pwd
                        pickle.dump(userdict, user_dir)
                        print("\033[0;32mRegistered successfully!\033[0m")
                        user_dir.close()
                        break
                    else:
                        print("\033[0;31mPassword mismatch!\033[0m")
                        pwd_ch = input("Re-enter your password: ")
                        continue
            elif readinfo["username"] == username:
                print("\033[0;31mUsername already exists!\033[0m")
                print("1. Exit")
                print("2. Proceed with registration")
                ch = input("\033[0;31mEnter your choice: \033[0m")
                if ch == "1":
                    break
                elif ch == "2":
                    username = input("Enter new username: ")
                    user_dir.close()
                    user_dir = open(r"user_dir.dat", "ab+")
                    pwd = input("Enter your password: ")
                    pwd_ch = input("Re-enter your password: ")
                    while True:
                        if pwd == pwd_ch:
                            userdict = {}
                            userdict["username"] = username
                            userdict["password"] = pwd
                            pickle.dump(userdict, user_dir)
                            print("\033[0;32mRegistered successfully!\033[0m")
                            user_dir.close()
                            break
                        else:
                            print("\033[0;31mPassword mismatch!\033[0m")
                            pwd_ch = input("Re-enter your password: ")
                            continue
            else:
                user_dir = open(r"user_dir.dat", "ab+")
                pwd = input("Enter your password: ")
                pwd_ch = input("Re-enter your password: ")
                while True:
                    if pwd == pwd_ch:
                        userdict = {}
                        userdict["username"] = username
                        userdict["password"] = pwd
                        pickle.dump(userdict, user_dir)
                        print("\033[0;32mRegistered successfully!\033[0m")
                        user_dir.close()
                        break
                    else:
                        print("\033[0;31mPassword mismatch!\033[0m")
                        pwd_ch = input("Re-enter your password: ")
                        continue
    except EOFError:
        user_dir.close()


def login():
    user_x = open(r"user_dir.dat", "rb")
    if os.path.getsize(r"user_dir.dat") == 0:
        print("\033[0;31mDirectory empty! Enter an username first.\033[0m")
        register_new()
    else:
        try:
            while True:
                username = input("Enter your username: ")
                readinfo1 = pickle.load(user_x)
                c = 0
                if readinfo1["username"] == username:
                    pwd = input("Enter your password: ")
                    while c < 5:
                        if readinfo1["password"] == pwd:
                            print("\033[0;32mLogged in!\033[0m")
                            break
                        else:
                            print("\033[0;31mWrong password!\033[0m")
                            print(5 - c, "tries left")
                            pwd = input("Re-enter your password: ")
                            c += 1
                            continue
                else:
                    print("\033[0;31mUsername not found!\033[0m")
                    ch = input("Register as new user? (y/n)\033[0m")
                    if ch in "Yy":
                        register_new()
                        break
                    else:
                        break
        except EOFError:
            user_x.close()


while True:
    print("1. Login")
    print("2. Register as new user")
    ch0 = input("\033[0;32mEnter your choice: \033[0m")
    if ch0 == "1":
        login()
    elif ch0 == "2":
        register_new()
