import pickle

with open(r"user_dir.dat", "rb+") as f:
    try:
        while True:
            print(pickle.load(f))
    except EOFError:
        f.close()
