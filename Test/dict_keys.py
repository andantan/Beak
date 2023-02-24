dictx = {
    "alpha": "yes",
    "beta": "no",
    "gamma": False
}

keys = ["alpha", "beta", "gamma"]

for key in keys:
    print(key in dictx)


print(keys in dictx.keys())