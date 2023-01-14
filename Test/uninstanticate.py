class Block:
    class Instanctiating:
        def __new__(cls: type[object], *args, **kwargs) -> type[object]:
            raise TypeError(f"{cls.__name__} can not be instanctiated")


class Test(Block.Instanctiating):
    @staticmethod
    def abc():
        pass


import traceback


if __name__ == "__main__":
    try:
        less = Test()

    except Exception as ERO:
        print(f"1. {ERO}")
        print(traceback.format_exc())