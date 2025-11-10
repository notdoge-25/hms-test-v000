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


import os, pickle

def pharmacy_management():
    print("1. View stock")
    print("2. Modify stock")
    print("3. Billing")
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
                price = float(input("\033[0;31mEnter MRP: \033[0m"))
                quantity = int(input("\033[0;31mEnter quantity: \033[0m"))
                medlist.append({"item_name": item_name, "item_id": item_id, "quantity": quantity, "price": price})
            with open("pharmacy.dat", "wb") as f:
                for med in medlist:
                    pickle.dump(med, f)
        elif ch == "3":
            print("Coming soon...")


def pharmacy_management():
    print("1. View stock")
    print("2. Modify stock")
    print("3. Billing")
    while True:
        ch = input("\033[0;36mEnter your choice: \033[0m")
        if ch == "1":
            try:
                with open(r"pharmacy.dat", "rb+") as f:
                    if os.path.getsize("pharmacy.dat") == 0:
                        print("Stock empty!")
                        continue
                    else:
                        try:
                            while True:
                                print(pickle.load(f))
                        except EOFError:
                            pass
            except FileNotFoundError:
                print("\033[0;31mPharmacy records file not found. Contact administrator.\033[0m")
                print("\033[0;31mLogging out...\033[0m")
                return ui_1()
        elif ch == "2":
            medlist = []
            try:
                if os.path.getsize("pharmacy.dat") > 0:
                    with open("pharmacy.dat", "rb") as f:
                        try:
                            while True:
                                medlist.append(pickle.load(f))
                        except EOFError:
                            pass
            except FileNotFoundError:
                print("Pharmacy records file not found. Create new? (y/n)\033[0m")
                while True:
                    if ch in "Yy":
                        f = open("pharmacy.dat", "ab")
                        f.close()
            item_name = input("\033[0;31mEnter name of item: \033[0m")
            item_id = input("\033[0;31mEnter id of item: \033[0m")
            for items in medlist:
                if items["item_id"] == item_id:
                    print("\033[0;33mItem already exists.\033[0m")
                    print("1. Restock or Refund")
                    print("2. Sell")
                        while True:
                            ch = input("\033[0;36mEnter your choice: \033[0m")
                            if ch == "1":
                                try:
                                    quantity = int(input("\033[0;31mEnter no of items added: \033[0m"))
                                    items["quantity"] += quantity
                                    break
                                except ValueError:
                                    print("\033[0;31mPlease enter only numeric!\033[0m")
                            elif ch == "2":
                                try:
                                    quantity = int(input("\033[0;31mEnter number of items sold: \033[0m"))
                                    items["quantity"] -= quantity
                                    break
                                except ValueError:
                                    print("\033[0;31mPlease enter only numeric!\033[0m")
            while True:
                try:
                    price = float(input("\033[0;31mEnter MRP: \033[0m"))
                    quantity = int(input("\033[0;31mEnter quantity: \033[0m"))
                    break
                except ValueError:
                    print("\033[0;31mPlease enter a valid quantity!\033[0m")
                ch = input("\033[0;36mConfirm entry? (y/n): \033[0m")
                if ch in "Yy":
                    break
                elif ch in "Nn":
                    continue
                else:
                    print("\033[0;31mInvalid choice! Try again!\033[0m")
            med = {"item_name": item_name, "item_id": item_id, "quantity": quantity, "price": price}
            medlist.append(med)
            with open("pharmacy.dat", "wb") as f:
                for items in medlist:
                    pickle.dump(items, f)

        elif ch == "3":
            print("Coming soon...")








