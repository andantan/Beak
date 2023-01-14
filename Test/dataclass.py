from dataclasses import dataclass


@dataclass
class PL_status:
    FM: bool = True
    LM: bool = True
    PL: bool = True
    PE: bool = False
    ED: bool = False
    LO: int = 0


    @property
    def is_first_audio(self) -> bool:
        return self.FM


    @is_first_audio.setter
    def is_first_audio(self, updated_FM: bool) -> None:
        if isinstance(updated_FM, bool):
            self.FM = updated_FM
        elif isinstance(updated_FM, type(None)):
            print("none")
        else:
            print("error", type(updated_FM))


def tossing_type(types: type) -> None:
    print(types)
        

if __name__ == "__main__":
    tossing_type(type(30))

    for i in range(0, 10):
        print(i % 3)
