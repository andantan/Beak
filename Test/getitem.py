from typing import List, Any


class Singleton(type):
    _instance = {}
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if not cls in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            
        return cls._instance[cls]



class Pool(metaclass=Singleton):
    def __init__(self) -> None:
        self.dicts = dict()

    
    def __setitem__(self, id: int) -> None:
        if id in self.dicts:
            raise AttributeError(f"Already allocated id: {id}")
        
        else:
            self.dicts.__setitem__(id, [id * 10])


    def __getitem__(self, id: int) -> List[int]:
        if id in self.dicts:
            return self.dicts.__getitem__(id)
        
        else:
            raise AttributeError("Id not founded")

    
    def get(self, id: int) -> List[int]:
        return self.__getitem__(id)

    
    def __delitem__(self, id: int) -> None:
        self.dicts.__delitem__(id)


    def __contains__(self, id: int) -> bool:
        return id in self.dicts

    
    def print(self) -> None:
        for k, v in self.dicts.items():
            print(f"{k}: {v}")
        else:
            print("================")



if __name__ == "__main__":
    pool1 = Pool()

    try:
        pool1.__setitem__(10)
        pool1.__setitem__(20)
    except AttributeError as e:
        print(e)

    pool1.print()
    
    print(pool1.__getitem__(10))

    pool2 = Pool()

    print(pool2.__getitem__(10))
    print(pool2.get(20))
    print(pool2.get(30))
