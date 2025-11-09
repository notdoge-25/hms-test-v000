import pickle

with open(r"emp_cred.dat", "rb+") as f:
    try:
        while True:
            print(pickle.load(f))
    except EOFError:
        f.close()
