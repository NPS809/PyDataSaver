class FieldAlreadyExist(Exception):
    def __init__(self):
        super().__init__("Поле с таким именем уже существует")


class ChapterAlreadyExist(Exception):
    def __init__(self):
        super().__init__("Раздел с таким именем уже существует")


class ChapterNotExist(Exception):
    def __init__(self):
        super().__init__("Раздела с таким именем не существует")


class FieldNotExist(Exception):
    def __init__(self):
        super().__init__("Полe с таким именем не существует")


class DataFileNotLoaded(Exception):
    def __init__(self):
        super().__init__("Файл данных не подгружен")


class DataFileNotFound(Exception):
    def __init__(self):
        super().__init__("Файл данных не найден")


class IncorrectName(Exception):
    def __init__(self):
        super().__init__("Такое имя нельзя использовать")
