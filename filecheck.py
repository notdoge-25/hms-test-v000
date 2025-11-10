import pickle
l = []
with open(r"pharmacy.dat", "rb+") as f:
    try:
        while True:
            print(pickle.load(f))
    except EOFError:
        pass

