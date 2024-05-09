class FieldAlreadyExistError(Exception):
    def __init__(self):
        super().__init__("\nПоле с таким именем уже существует")


class ChapterAlreadyExistError(Exception):
    def __init__(self):
        super().__init__("\nРаздел с таким именем уже существует")


class ChapterNotExistError(Exception):
    def __init__(self):
        super().__init__("\nРаздела с таким именем не существует")


class FieldNotExistError(Exception):
    def __init__(self):
        super().__init__("\nПолe с таким именем не существует")


class DataFileNotLoadedError(Exception):
    def __init__(self):
        super().__init__("\nФайл данных не подгружен")


class DataFileNotFoundError(Exception):
    def __init__(self):
        super().__init__("\nФайл данных не найден")


class IncorrectNameError(Exception):
    def __init__(self, extra_info: str):
        super().__init__(f"\nТакое имя нельзя использовать: {extra_info}")


class DataFileSyntaxError(Exception):
    def __init__(self, extra_info: str):
        super().__init__(f"\nНеправильный синтаксис файла данных\n---> {extra_info}")
