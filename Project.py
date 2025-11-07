import pickle
import os

file = open(r"user_dir.dat", "ab+")
file.close()
file = open(r"emp_master.dat", "ab+")
file.close()
file = open(r"inventory_dir.dat", "ab+")
file.close()
cur_uid = ''

def register_new():
    username = input("Enter name: ")
    uid = input("Enter UID: ")
    users = []
    if os.path.getsize("user_dir.dat") > 0:
        with open("user_dir.dat", "rb") as f:
            try:
                while True:
                    x = pickle.load(f)
                    users.append(x)
            except EOFError:
                pass
    for user in users:
        if user["uid"] == uid:
            print("\033[0;31mUID already exists!\033[0m")
            print("1. Exit")
            print("2. Try a different UID")
            ch = input("\033[0;31mEnter your choice: \033[0m")
            if ch == "1":
                return
            elif ch == "2":
                return register_new()
    while True:
        pwd = input("Enter your password: ")
        pwd_ch = input("Re-enter your password: ")
        if pwd == pwd_ch:
            new_user = {"uid": uid, "name": username, "password": pwd}
            with open("user_dir.dat", "ab") as f:
                pickle.dump(new_user, f)
            print("\033[0;32mRegistered successfully!\033[0m")
            break
        else:
            print("\033[0;31mPassword mismatch! Try again.\033[0m")


def login():
    global cur_uid
    if os.path.getsize("user_dir.dat") == 0:
        print("\033[0;31mDirectory empty! Please register first.\033[0m")
        register_new()
    uid = input("Enter your UID: ")
    users = []
    with open("user_dir.dat", "rb") as f:
        try:
            while True:
                users.append(pickle.load(f))
        except EOFError:
            pass
    for user in users:
        if user["uid"] == uid:
            cur_uid = uid
            for i in range(5):
                pwd = input("Enter your password: ")
                if user["password"] == pwd:
                    print("\033[0;32mLogged in successfully!\033[0m")
                    print(f"\033[0;32mWelcome back {user["name"]}!\033[0m")
                    return menu()
                else:
                    print(f"\033[0;31mWrong password! {4 - i} tries left.\033[0m")
            print("\033[0;31mToo many failed attempts. Try again later.\033[0m")
            return None
    else:
        print("\033[0;31mUsername not found!\033[0m")
        ch = input("Register as new user? (y/n): ")
        if ch in "Yy":
            return register_new()
        elif ch in "Nn":
            return None
        return None

def ui_1():
    print("1. Administrator login")
    print("2. Register new admin account")
    print("3. Employee login")
    print("4. Exit")
    ch0 = input("\033[0;32mEnter your choice: \033[0m")
    if ch0 == "1":
        login()
    elif ch0 == "2":
        register_new()
    elif ch0 == "3":
        emp_menu()
    elif ch0 == "4":
        exit()

def menu():
    print("\033[1;33mWhat do you want to work on?\033[0m")
    print("1. Employee Management")
    print("2. Patient Management")
    print("3. Inventory Management")
    print("4. Transaction Management")
    print("5. Pharmacy Management")
    print("6. Change password")
    print("7. Remove account")
    print("8. Logout")
    ch = input("\033[0;36mEnter your choice: \033[0m")
    if ch == "1":
        return employee_management()
    elif ch == "2":
        return patient_management()
    elif ch == "3":
        return inventory_management()
    elif ch == "4":
        return transaction_management()
    elif ch == "6":
        return change_password()
    elif ch == "7":
        return remove_account()
    elif ch == "8":
        ch = input("\033[0;33mConfirm logout? (y/n) \033[0m")
        if ch in "Yy":
            print("\033[0;34mLogged out! \033[0m")
            return ui_1()
        elif ch in "Nn":
            return menu()
        return menu()
    else:
        return menu()

def emp_menu():
    pass

def employee_management():
    print("1. Create new entry")
    print("2. Remove employee")
    print("3. Back")
    ch = input("\033[0;36mEnter your choice: \033[0m")
    if ch == "1":
        print("1. Doctor")
        print("2. Nurse")
        print("3. Receptionist")
        print("4. ")
        name1 = input("Enter employee name: ")
        desig = input("Enter employee designation: ")
        empid = input("Enter employee ID: ")
        new_entry = {"empid": empid, "name": name1, "designation": desig}



        with open("emp_master.dat", "ab+") as f:
            try:
                while True:
                    pass
            except EOFError:
                pass



def patient_management():
    pass

def inventory_management():
    pass

def transaction_management():
    pass

def pharmacy_management():
    pass

def change_password():
    users = []
    with open("user_dir.dat", "rb") as f:
        try:
            while True:
                users.append(pickle.load(f))
        except EOFError:
            pass
    for user in users:
        if user["uid"] == cur_uid:
            while True:
                new_password = input("Enter new password: ")
                if new_password == user["password"]:
                    print("\033[0;33mNew and old passwords cannot be same!\033[0m")
                    continue
                else:
                    new_password_check = input("Re-enter new password: ")
                    if new_password_check == new_password:
                        user["password"] = new_password
                        print("\033[0;32mPassword changed successfully!\033[0m")
                        break
                    else:
                        print("\033[0;31mPassword mismatch! Try again. \033[0m")
                        continue
    with open("user_dir.dat", "wb") as f:
        for user in users:
            pickle.dump(user, f)
    return menu()

def remove_account():
    users = []
    with open("user_dir.dat", "rb") as f:
        try:
            while True:
                users.append(pickle.load(f))
        except EOFError:
            pass
    for user in users:
        if user["uid"] == cur_uid:
            ch = input("Are you sure you want to remove the account? (y/n): ")
            if ch in "Yy":
                users.remove(user)
            else:
                return menu()
    with open("user_dir.dat", "wb") as f:
        for user in users:
            pickle.dump(user, f)
            print("\033[0;33mUser removed successfully!\033[0m")
    return ui_1()



while True:
    ui_1()

