import pickle
import os
import getpass


file = open(r"admin_dir.dat", "ab")
file.close()
file = open(r"emp_dir.dat", "ab")
file.close()
file = open(r"emp_cred.dat", "ab")
file.close()
file = open(r"inventory_dir.dat", "ab")
file.close()
file = open(r"patient_rec.dat", "ab")
file.close()
file = open(r"pharmacy.dat", "ab")
cur_uid = None
cur_pwd = None
cur_empid = None
cur_user = None
master_pwd = "12345678"

def ui_1():
    print("1. Administrator login")
    print("2. Register new admin account")
    print("3. Employee login")
    print("4. Exit")
    ch0 = input("\033[0;32mEnter your choice: \033[0m")
    if ch0 == "1":
        return login()
    elif ch0 == "2":
        for i in range(3):
            pwd_check = input("\033[0;32mEnter master password: \033[0m")
            if pwd_check == master_pwd:
                return register_new()
            else:
                print(f"\033[0;31mWrong password! {2-i} tries left.\033[0m")
    elif ch0 == "3":
        return emp_login()
    elif ch0 == "4":
        exit()
    else:
        print("\033[0;31mInvalid choice!\033[0m")
        return ui_1()
    return ui_1()


def register_new():
    username = input("Enter name: ")
    uid = input("Enter UID: ")
    users = []
    try:
        if os.path.getsize("admin_dir.dat") > 0:
            with open("admin_dir.dat", "rb") as f:
                try:
                    while True:
                        x = pickle.load(f)
                        users.append(x)
                except EOFError:
                    pass
    except FileNotFoundError:
        ch = input("\033[0;31mAdministrator directory file not found. Create new? (y/n)\033[0m")
        if ch in "Yy":  
            f = open("admin_dir.dat", "wb")
            f.close()
            return register_new()
        if ch in "Nn":
            print("\033[0;31mExiting... Reason: FileNotFoundError. Create new or contact IT Admin. \033[0m")
            exit()
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
            with open("admin_dir.dat", "ab") as f:
                pickle.dump(new_user, f)
            print("\033[0;32mRegistered successfully!\033[0m")
            return ui_1()
        else:
            print("\033[0;31mPassword mismatch! Try again.\033[0m")


def login():
    global cur_uid
    global cur_pwd
    global cur_user
    if os.path.getsize("admin_dir.dat") == 0:
        print("\033[0;31mDirectory empty! Please register first.\033[0m")
        pwd_check = input("\033[0;31mEnter master password: \033[0m")
        for i in range(3):
            if pwd_check == master_pwd:
                register_new()
            else:
                print(f"\033[0;31mWrong password! {3-i} tries left.\033[0m")
    uid = input("Enter your UID: ")
    users = []
    with open("admin_dir.dat", "rb") as f:
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
                    cur_pwd = pwd
                    print("\033[0;32mLogged in successfully!\033[0m")
                    print(f"\033[0;32mWelcome back {user["name"]}!\033[0m")
                    cur_user = "admin"
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


def menu():
    print("\033[1;33mWhat do you want to work on?\033[0m")
    print("1. Employee Management")
    print("2. Patient Management")
    print("3. Inventory Management")
    print("4. Pharmacy Management")
    print("5. Change password")
    print("6. Remove account")
    print("7. Logout")
    ch = input("\033[0;36mEnter your choice: \033[0m")
    if ch == "1":
        return employee_management()
    elif ch == "2":
        return patient_management()
    elif ch == "3":
        return inventory_management()
    elif ch == "4":
        return pharmacy_management()
    elif ch == "5":
        return change_password()
    elif ch == "6":
        return remove_account()
    elif ch == "7":
        ch = input("\033[0;33mConfirm logout? (y/n) \033[0m")
        if ch in "Yy":
            print("\033[0;34mLogged out! \033[0m")
            return ui_1()
        elif ch in "Nn":
            return menu()
        return menu()
    else:
        print("\033[0;31mInvalid choice!\033[0m")
        return menu()

def employee_management():
    while True:
        print("1. Create new entry")
        print("2. Remove employee")
        print("3. View all entries")
        print("4. Back")
        ch = input("\033[0;36mEnter your choice: \033[0m")
        if ch == "1":
            return reg_new_empl()
        elif ch == "2":
            return remove_empl()
        elif ch == "3":
            try:
                if os.path.getsize("emp_dir.dat") == 0:
                    print("\033[0;31mDirectory empty! Please register first.\033[0m")
                else:
                    with open("emp_dir.dat", "rb+") as f:
                        try:
                            while True:
                                print(pickle.load(f))
                        except EOFError:
                            pass
            except FileNotFoundError:
                print("\033[0;31mDirectory not found! Creating new...\033[0m")
                f = open("emp_dir.dat", "ab")
                f.close()
        elif ch == "4":
            return menu()
        else:
            print("\033[0;31mInvalid choice!\033[0m")



def reg_new_empl():
    empid = input("Enter employee ID: ")
    emplist = []
    try:
        if os.path.getsize("emp_dir.dat") > 0:
            with open("emp_dir.dat", "rb") as f:
                try:
                    while True:
                        emplist.append(pickle.load(f))
                except EOFError:
                    pass
        for emp in emplist:
            if emp["empid"] == empid:
                print("\033[0;32mEmployee ID already exists!\033[0m")
                print("1. Back")
                print("2. Try a different UID")
                ch = input("\033[0;31mEnter your choice: \033[0m")
                if ch == "1":
                    return employee_management()
                elif ch == "2":
                    return reg_new_empl()
    except FileNotFoundError:
        print("\033[0;31mEmployee directory file not found. Creating new...\033[0m")
        open("emp_dir.dat", "wb").close()
    name1 = input("Enter employee name: ")
    print("\033[0;33mChoose designation: \033[0m")
    print("1. Doctor")
    print("2. Nurse")
    print("3. Receptionist")
    print("4. Surgeon")
    print("5. Pharmacist")
    while True:
        ch = input("\033[0;36mEnter your choice: \033[0m")
        if ch == "1":
            designation = "doctor"
            break
        elif ch == "2":
            designation = "nurse"
            break
        elif ch == "3":
            designation = "receptionist"
            break
        elif ch == "4":
            designation = "surgeon"
            break
        elif ch == "5":
            designation = "pharmacist"
            break
        else:
            print("\033[0;31mInvalid choice!\033[0m")
    spec = None
    if designation == "doctor":
        print("\033[0;33mChoose specialty: \033[0m")
        while True:
            print("1. Cardiologist")
            print("2. Neurologist")
            print("3. Nephrologist")
            print("4. Gynaecologist")
            print("5. Paediatrician")
            print("6. Dermatologist")
            print("7. Orthopaedist")
            print("8. Medicine")
            ch = input("\033[0;36mSo, who's it gonna be?: \033[0m")
            if ch == "1":
                spec = "Cardiologist"
                break
            elif ch == "2":
                spec = "Neurologist"
                break
            elif ch == "3":
                spec = "Nephrologist"
                break
            elif ch == "4":
                spec = "Gynaecologist"
                break
            elif ch == "5":
                spec = "Paediatrician"
                break
            elif ch == "6":
                spec = "Dermatologist"
                break
            elif ch == "7":
                spec = "Orthopaedist"
                break
            elif ch == "8":
                spec = "Medicine"
                break
            else:
                print("\033[0;31mPlease enter a valid choice!!\033[0m")
    new_entry = {"empid": empid, "name": name1, "designation": designation, "specialty": spec, "pwd" : None}
    with open("emp_dir.dat", "ab+") as f:
        pickle.dump(new_entry, f)
    print("\033[0;32mEmployee ID saved!. Account Created!\033[0m")
    return employee_management()


def remove_empl():
    empid = input("Enter employee ID: ")
    emplist = []
    try:
        with open("emp_dir.dat", "rb") as f:
            try:
                while True:
                    emplist.append(pickle.load(f))
            except EOFError:
                pass
    except FileNotFoundError:
        print("\033[0;31mEmployee directory file not found. Cannot remove account. Contact administrator.\033[0m")
        print("\033[0;31mLogging out...\033[0m")
        return ui_1()
    target_empl = None
    for emp in emplist:
        if emp["empid"] == empid:
            target_empl = emp
            break
    if target_empl is None:
        print("\033[0;31mInvalid empID!\033[0m")
        print("1. Go back")
        print("2. Try a different empID")
        ch = input("\033[0;36mEnter your choice: \033[0m")
        if ch == "1":
            return employee_management()
        elif ch == "2":
            return remove_empl()
        else:
            print("\033[0;31mInvalid choice!\033[0m")
            return employee_management()
    ch = input("\033[0;36mAre you sure you want to remove the account? (y/n) \033[0m")
    if ch in "Yy":
        for i in range(3):
            pwd_check = input("\033[0;31mEnter current admin password: \033[0m")
            if pwd_check == cur_pwd:
                emplist.remove(target_empl)
                with open("emp_dir.dat", "wb") as f:
                    for emp in emplist:
                        pickle.dump(emp, f)
                print("\033[0;32mEmployee removed successfully!\033[0m")
                return employee_management()
            else:
                print(f"\033[0;31mWrong password! {2-i} tries left.\033[0m")
        return None
    else:
        return employee_management()


def patient_management():
    print("coming soon...")
    return menu()


def inventory_management():
    print("coming soon...")
    return menu()


def pharmacy_management():
    print("1. View stock")
    print("2. Modify stock")
    print("3. Billing")
    if cur_user == "admin":
        print("4. Go back")
    elif cur_user == "pharmacist":
        print("4. Logout")
    while True:
        ch = input("\033[0;36mEnter your choice: \033[0m")
        if ch == "1":
            if not os.path.exists("pharmacy.dat") or os.path.getsize("pharmacy.dat") == 0:
                print("Stock empty!")
                continue
            with open("pharmacy.dat", "rb") as f:
                try:
                    while True:
                        print(pickle.load(f))
                except EOFError:
                    pass
        elif ch == "2":
            medlist = []
            if os.path.exists("pharmacy.dat") and os.path.getsize("pharmacy.dat") > 0:
                with open("pharmacy.dat", "rb") as f:
                    try:
                        while True:
                            medlist.append(pickle.load(f))
                    except EOFError:
                        pass
            item_name = input("\033[0;31mEnter name of item: \033[0m")
            item_id = input("\033[0;31mEnter id of item: \033[0m")
            found = False
            for items in medlist:
                if items["item_id"] == item_id:
                    found = True
                    print("\033[0;33mItem already exists.\033[0m")
                    print("1. Restock or Refund")
                    print("2. Sell")
                    sub_ch = input("\033[0;36mEnter your choice: \033[0m")
                    if sub_ch == "1":
                        quantity = int(input("\033[0;31mEnter no of items added: \033[0m"))
                        items["quantity"] += quantity
                    elif sub_ch == "2":
                        quantity = int(input("\033[0;31mEnter number of items sold: \033[0m"))
                        items["quantity"] -= quantity
            if not found:
                while True:
                    try:
                        price = float(input("\033[0;31mEnter MRP: \033[0m"))
                        quantity = int(input("\033[0;31mEnter quantity: \033[0m"))
                        break
                    except ValueError:
                        print("\033[0;31mPlease enter proper data type! (Price - Float; Quantity - Integer\033[0m")
                med = {"item_name": item_name, "item_id": item_id, "quantity": quantity, "price": price}
                medlist.append(med)
            with open("pharmacy.dat", "wb") as f:
                for med in medlist:
                    pickle.dump(med, f)
                    print("\033[0;32mItem added to pharmacy.dat\033[0m")
        elif ch == "3":
            print("Coming soon...")
        elif ch == "4" and cur_user == "pharmacist":
            print("\033[0;33mLogging out!\033[0m")
            return None
        elif ch == "4" and cur_user == "admin":
            return menu()
        else:
            print("\033[0;31mInvalid choice!\033[0m")

def change_password():
    users = []
    with open("admin_dir.dat", "rb") as f:
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
    with open("admin_dir.dat", "wb") as f:
        for user in users:
            pickle.dump(user, f)
    return menu()


def remove_account():
    users = []
    uid = cur_uid
    try:
        with open("admin_dir.dat", "rb") as f:
            try:
                while True:
                    users.append(pickle.load(f))
            except EOFError:
                pass
    except FileNotFoundError:
        print("\033[0;31mAdmin directory file not found. Cannot remove account.\033[0m")
        return menu()
    target_user = None
    for user in users:
        if user["uid"] == uid:
            target_user = user
            break
    if not target_user:
        print("\033[0;31mInvalid UID!\033[0m")
        print("1. Go back")
        print("2. Try a different UID")
        ch = input("\033[0;36mEnter your choice: \033[0m")
        if ch == "1":
            return menu()
        elif ch == "2":
            return remove_account()
        else:
            print("\033[0;31mInvalid choice!\033[0m")
            return menu()
    def remove_acc_sub():
        for i in range(3):
            pwd = input("Enter password: ")
            if target_user["password"] == pwd:
                users.remove(target_user)
                with open("admin_dir.dat", "wb") as f:
                    for user in users:
                        pickle.dump(user, f)
                print("\033[0;33mUser removed successfully!\033[0m")
                if uid == cur_uid:
                    print("\033[0;34mLogged out!\033[0m")
                    return ui_1()
                else:
                    return menu()
            else:
                print(f"\033[0;31mWrong password! {2 - i} tries left.\033[0m")
        print("\033[0;31mToo many failed attempts. Account not removed.\033[0m")
        return menu()
    ch = input("Are you sure you want to remove the current account and logout? (y/n): ")
    if ch in "Yy":
        return remove_acc_sub()
    elif ch in "Nn":
        return menu()
    else:
        print("\033[0;31mEnter (y/n)!\033[0m")
        return menu()



def emp_login():
    if os.path.getsize("emp_dir.dat") == 0:
        print("\033[0;31mEmployee directory empty! Please contact administrator!\033[0m")
        return ui_1()
    empid = input("Enter your empID: ")
    emp_list = []
    try:
        with open("emp_dir.dat", "rb") as f:
            try:
                while True:
                    emp_list.append(pickle.load(f))
            except EOFError:
                pass
    except FileNotFoundError:
        print("\033[0;31mEmployee credential file not found. Contact administrator.\033[0m")
        return ui_1()
    for emp in emp_list:
        global cur_empid
        global cur_user
        if emp["empid"] == empid:
            if not emp["pwd"]:
                print(f"\033[0;36mLogging in for the first time...create new password.")
                while True:
                    pwd = input("Enter your password: ")
                    pwd_ch = input("Re-enter your password: ")
                    if pwd == pwd_ch:
                        emp["pwd"] = pwd
                        with open("emp_cred.dat", "wb") as f:
                            for entry in emp_list:
                                pickle.dump(entry, f)
                        print("\033[0;32mPassword created successfully!\033[0m")
                        return ui_1()
                    else:
                        print("\033[0;31mPassword mismatch! Try again.\033[0m")
            else:
                for i in range(5):
                    pwd = input("Enter your password: ")
                    if emp["pwd"] == pwd:
                        cur_empid = empid
                        print("\033[0;32mLogged in successfully!\033[0m")
                        print(f"\033[0;32mWelcome back!\033[0m")
                        if empid[0:3] != "pha":
                            print("1. Patient Management")
                            print("2. Change Password")
                            print("3. Logout")
                            while True:
                                ch = input("Enter your choice: ")
                                if ch == "1":
                                    return patient_management()
                                elif ch == "2":
                                    return change_pwd_empl()
                                elif ch == "3":
                                    print("\033[0;33mLogging out!\033[0m")
                                    return ui_1()
                                else:
                                    print("\033[0;31mInvalid choice!\033[0m")
                        elif emp["empid"][:3] == "pha":
                            cur_user = "pharmacist"
                            return pharmacy_management()
                    else:
                        print(f"\033[0;31mWrong password! {4 - i} tries left.\033[0m")
                print("\033[0;31mToo many failed attempts. Try again later.\033[0m")
                return ui_1()
    else:
        print("\033[1;31mNot registered! Contact administrator!\033[0m")
        return ui_1()

def change_pwd_empl():
    emplist = []
    with open("emp_cred.dat", "rb") as f:
        try:
            while True:
                emplist.append(pickle.load(f))
        except EOFError:
            pass
    for emp in emplist:
        if emp["empid"] == cur_empid:
            while True:
                new_password = input("Enter new password: ")
                if new_password == emp["pwd"]:
                    print("\033[0;33mNew and old passwords cannot be same!\033[0m")
                    continue
                else:
                    new_password_check = input("Re-enter new password: ")
                    if new_password_check == new_password:
                        emp["pwd"] = new_password
                        print("\033[0;32mPassword changed successfully!\033[0m")
                        break
                    else:
                        print("\033[0;31mPassword mismatch! Try again. \033[0m")
                        continue
    with open("emp_cred.dat", "wb") as f:
        for emp in emplist:
            pickle.dump(emp, f)
    return menu()






while True:
    ui_1()





