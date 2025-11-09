print("\033[1;31mThis text is red and bold.\033[0m")
print("\033[0;32mThis text is green.\033[0m")
print("\033[1;33;40mBright Yellow text on Black background.\033[0m")
'''for key, value in i:
    if key == username:
        pwd = input("Enter your password")
        for i in range(3):
            if pwd == readinfo[value]:
                print("\033[0;32mLogged in successfully!\033[0m")
                break
            else:
                print("\033[0;31mWrong password!\033[0m")
                print(3 - i, "tries left")
                continue
    else:
        ch = input("\033[1;31mUsername not found. Want to register as new user? (y/n)\033[0m")
    if ch in "Yy":
        register_new()
    elif ch in "Nn":
        break'''


def remove_empl():
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
    except FileNotFoundError:
        print("\033[0;31mEmployee directory file not found. Cannot remove account. Contact administrator.\033[0m")
        print("\033[0;31mLogging out and exiting...\033[0m")
        exit()
    target_empl = ''
    for emp in emplist:
        if emp["empid"] == empid:
            target_empl = emp
            break
    if not target_empl:
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
            print(cur_pwd)
            if pwd_check == cur_pwd:
                emplist.remove(target_empl)
                with open("emp_dir.dat", "wb") as f:
                    for emp in emplist:
                        pickle.dump(emp, f)
                        f.close()
            else:
                print(f"\033[0;31mWrong password! {2-i} tries left.\033[0m")
        return None
    elif ch in "Nn":
        return employee_management()