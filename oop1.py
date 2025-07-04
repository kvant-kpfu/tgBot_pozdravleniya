class Kvantovec:
    # ПОЛЯ КЛАССА
    name = ''
    data_of_birth = 0
    napravlenie: str
    phone_number: int
    mail: str
    test_scorel: int 

    # методы класса
    def passed():
        if test_scorel >= 115:
            return True
        elif test_scorel < 115:
            return False