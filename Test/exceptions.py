a = (
    {
        "a": 1,
        "b": 2
    } ,
)


a.__getitem__(0).__setitem__("a", 3)

print(a)