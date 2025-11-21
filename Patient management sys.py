import pickle
import os

PATIENT_FILE = "patient_rec.dat"
WARD_FILE = "inventory_dir.dat"

def load_patients():
    """Load patient records from file."""
    if os.path.exists(PATIENT_FILE):
        with open(PATIENT_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def load_wards():
    """Load ward inventory from file."""
    if os.path.exists(WARD_FILE):
        with open(WARD_FILE, "rb") as f:
            return pickle.load(f)
    # Initialize with empty wards if file doesn't exist
    return {
        "ICU": [],
        "General": [],
        "Isolation": []
    }

def save_wards(data):
    """Save ward inventory to file."""
    with open(WARD_FILE, "wb") as f:
        pickle.dump(data, f)

def suggest_ward(patient_info):
    """Suggest ward based on patient condition."""
    if patient_info["contagious"]:
        return "Isolation"
    elif "icu" in patient_info["disease"].lower() or "critical" in patient_info["disease"].lower():
        return "ICU"
    else:
        return "General"

def inventory_management():
    wards = load_wards()
    patients = load_patients()

    while True:
        print("\n--- Ward Inventory Management ---")
        print("1. Assign Patient to Ward (Auto-Suggest)")
        print("2. Remove Patient from Ward")
        print("3. View Ward Details")
        print("4. Generate Hospital Report")
        print("5. Generate Doctor-wise Report")
        print("6. Generate Speciality-wise Report")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            pid = input("Enter Patient ID: ")
            if pid not in patients:
                print("Patient not found in patient records!")
                continue

            patient_info = patients[pid]
            suggested_ward = suggest_ward(patient_info)

            print(f"Suggested Ward for {patient_info['name']} (Disease: {patient_info['disease']}): {suggested_ward}")
            ward = input(f"Enter ward name (press Enter to accept {suggested_ward}): ").capitalize()
            if ward == "":
                ward = suggested_ward

            if ward not in wards:
                print("Invalid ward name!")
                continue

            patient_entry = {
                "id": pid,
                "name": patient_info["name"],
                "disease": patient_info["disease"],
                "doctor": patient_info["doctor"],
                "speciality": patient_info["speciality"],
                "contagious": patient_info["contagious"]
            }

            wards[ward].append(patient_entry)
            save_wards(wards)
            print(f"Patient {patient_info['name']} (ID: {pid}) assigned to {ward} ward.")

        elif choice == "2":
            ward = input("Enter ward name: ").capitalize()
            if ward not in wards:
                print("Invalid ward name!")
                continue

            pid = input("Enter Patient ID to remove: ")
            found = False
            for patient in wards[ward]:
                if patient["id"] == pid:
                    wards[ward].remove(patient)
                    save_wards(wards)
                    print(f"Patient {patient['name']} (ID: {pid}) removed from {ward} ward.")
                    found = True
                    break
            if not found:
                print("Patient not found in this ward.")

        elif choice == "3":
            print("\n--- Ward Details ---")
            for ward, patients_list in wards.items():
                print(f"\n{ward} Ward:")
                if patients_list:
                    for p in patients_list:
                        print(f"  ID: {p['id']}, Name: {p['name']}, Disease: {p['disease']}, Doctor: {p['doctor']}, Speciality: {p['speciality']}")
                else:
                    print("  No patients assigned.")

        elif choice == "4":
            print("\n--- Hospital Report ---")
            total_patients = sum(len(patients_list) for patients_list in wards.values())
            contagious_count = sum(
                1 for patients_list in wards.values() for p in patients_list if p.get("contagious")
            )
            non_contagious_count = total_patients - contagious_count

            print(f"Total Patients: {total_patients}")
            print(f"Contagious Patients: {contagious_count}")
            print(f"Non-Contagious Patients: {non_contagious_count}")

            for ward, patients_list in wards.items():
                print(f"{ward} Ward: {len(patients_list)} patients")

        elif choice == "5":
            print("\n--- Doctor-wise Report ---")
            doctor_report = {}
            for ward, patients_list in wards.items():
                for p in patients_list:
                    doctor = p["doctor"]
                    if doctor not in doctor_report:
                        doctor_report[doctor] = {"total": 0, "wards": {"ICU": 0, "General": 0, "Isolation": 0}}
                    doctor_report[doctor]["total"] += 1
                    doctor_report[doctor]["wards"][ward] += 1

            if doctor_report:
                for doctor, stats in doctor_report.items():
                    print(f"\nDoctor {doctor}: {stats['total']} patients total")
                    for ward, count in stats["wards"].items():
                        if count > 0:
                            print(f"  {ward} Ward: {count} patients")
            else:
                print("No patients assigned to any doctor yet.")

        elif choice == "6":
            print("\n--- Speciality-wise Report ---")
            speciality_report = {}
            for ward, patients_list in wards.items():
                for p in patients_list:
                    speciality = p.get("speciality", "Unknown")
                    if speciality not in speciality_report:
                        speciality_report[speciality] = {"total": 0, "wards": {"ICU": 0, "General": 0, "Isolation": 0}}
                    speciality_report[speciality]["total"] += 1
                    speciality_report[speciality]["wards"][ward] += 1

            if speciality_report:
                for speciality, stats in speciality_report.items():
                    print(f"\nSpeciality {speciality}: {stats['total']} patients total")
                    for ward, count in stats["wards"].items():
                        if count > 0:
                            print(f"  {ward} Ward: {count} patients")
            else:
                print("No patients assigned to any speciality yet.")

        elif choice == "7":
            print("Exiting Ward Inventory Management...")
            break

        else:
            print("Invalid choice. Try again.")

import pickle
import os

DATA_FILE = "pharmacy.dat"

def load_stock(file=DATA_FILE):
    """Load entire stock list from file."""
    if os.path.exists(file) and os.path.getsize(file) > 0:
        with open(file, "rb") as f:
            return pickle.load(f)
    return []

def save_stock(stock, file=DATA_FILE):
    """Save entire stock list to file."""
    with open(file, "wb") as f:
        pickle.dump(stock, f)

def view_stock():
    stock = load_stock()
    if not stock:
        print("\033[0;31mStock empty!\033[0m")
        return
    print("\n--- Current Stock ---")
    for med in stock:
        print(f"Item: {med['item_name']} | ID: {med['item_id']} | Qty: {med['quantity']} | Price: {med['price']}")

def modify_stock():
    stock = load_stock()
    item_name = input("Enter name of item: ")
    item_id = input("Enter id of item: ")

    found = False
    for med in stock:
        if med["item_id"] == item_id:
            found = True
            print("\033[0;33mItem already exists.\033[0m")
            print("1. Restock or Refund")
            print("2. Sell")
            sub_ch = input("Enter your choice: ")
            if sub_ch == "1":
                quantity = int(input("Enter number of items added: "))
                med["quantity"] += quantity
            elif sub_ch == "2":
                quantity = int(input("Enter number of items removed: "))
                if med["quantity"] <= 0:
                    print("\033[0;31mOut of stock!\033[0m")
                elif med["quantity"] < quantity:
                    print("\033[0;31mNot enough stock!\033[0m")
                else:
                    med["quantity"] -= quantity
            break

    if not found:
        while True:
            try:
                price = float(input("Enter MRP: "))
                quantity = int(input("Enter quantity: "))
                break
            except ValueError:
                print("Please enter proper data type! (Price - Float; Quantity - Integer)")
        med = {"item_name": item_name, "item_id": item_id, "quantity": quantity, "price": price}
        stock.append(med)

    save_stock(stock)
    print("\033[0;32mOperation succeeded!\033[0m")

def billing():
    stock = load_stock()
    if not stock:
        print("No stock available!")
        return

    print("\n--- Available Medicines ---")
    for med in stock:
        print(f"Item: {med['item_name']} | ID: {med['item_id']} | Qty: {med['quantity']} | Price: {med['price']}")

    cart = []
    while True:
        med_id = input("Enter item id: ")
        found = False
        for item in stock:
            if item["item_id"] == med_id:
                found = True
                qty = int(input("Enter quantity: "))
                if item["quantity"] >= qty:
                    cart.append({"item_name": item["item_name"], "item_id": item["item_id"],
                                 "quantity": qty, "price": item["price"]})
                    item["quantity"] -= qty
                else:
                    print("Not enough stock!")
        if not found:
            print("Item not found!")

        more = input("Add more? (y/n): ").lower()
        if more != "y":
            break

    # Print bill
    total = sum(c["quantity"] * c["price"] for c in cart)
    print("\n--- BILL ---")
    for c in cart:
        print(f"{c['item_name']} x {c['quantity']} @ {c['price']} = {c['quantity']*c['price']}")
    print(f"TOTAL: {total}")

    save_stock(stock)

def pharmacy_management(cur_user):
    while True:
        print("\n--- Pharmacy Management ---")
        print("1. View stock")
        print("2. Modify stock")
        print("3. Billing")
        print("4. Logout" if cur_user == "pharmacist" else "4. Go back")

        ch = input("Enter your choice: ")

        if ch == "1":
            view_stock()
        elif ch == "2":
            modify_stock()
        elif ch == "3":
            billing()
        elif ch == "4":
            if cur_user == "pharmacist":
                print("Logging out!")
                return None
            else:
                return menu()  # assuming you have a menu() function for admin
        else:
            print("Invalid choice!")