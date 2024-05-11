from string import ascii_letters
from DataSaver.errors import *
from DataSaver.classes import *


class DS:
    __logs_enabled: bool = False
    __isLoaded: bool = False
    __path_to_file: str = ""
    __chapters: list[Chapter] = []
    __av_chars = list(ascii_letters) + ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ", "_"]

    @staticmethod
    def Log(message: str):
        if DS.__logs_enabled:
            print(f"[datasaver]: {message}")

    @staticmethod
    def EnableLogs():
        DS.__logs_enabled = True

    @staticmethod
    def DisableLogs():
        DS.__logs_enabled = False

    @staticmethod
    def __CheckName(name: str):
        """DataSaver private method"""
        DS.Log(f"Проверка имени '{name}' на доступность")
        if not name:
            raise IncorrectNameError(name)
        for char in name:
            if char not in DS.__av_chars:
                raise IncorrectNameError(name)
        DS.Log("Имя доступно!")

    @staticmethod
    def __AddChapter(chapter: Chapter):
        """DataSaver private method"""
        DS.Log(f"Попытка добавить новый раздел с именем '{chapter.name}'")
        if chapter in DS.__chapters:
            raise ChapterAlreadyExistError()
        DS.__chapters.append(chapter)
        DS.Log(f"Добавлен новый раздел с именем '{chapter.name}'")

    @staticmethod
    def __CheckWordload():
        """DataSaver private method"""
        if not DS.__isLoaded:
            raise DataFileNotLoadedError()

    @staticmethod
    def Load(path_to_file: str):
        DS.Log(f"Попытка загрузить файл '{path_to_file}'")
        try:
            with open(path_to_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
            chapters = []
            for i in range(len(lines)):
                if "#" in lines[i]:
                    for j in range(i, len(lines)):
                        if "}" in lines[j]:
                            chapters.append([i, j])
                            break
            chapters = [lines[a:b] for a, b in chapters]

            for chapter in chapters:
                chapter_name = chapter[0].strip().removeprefix("#").removesuffix("{").strip()

                DS.__CheckName(chapter_name)
                chpt = Chapter(chapter_name)

                for field in chapter[1:]:
                    if field.strip():
                        try:
                            name, value = field.strip().split(":")
                            name = name.strip()
                            value = value.strip()
                            DS.__CheckName(name)
                            chpt.Add(name, value)
                        except SyntaxError:
                            raise DataFileSyntaxError(f"'{field.strip()}'")
                        except TypeError:
                            raise DataFileSyntaxError(f"'{field.strip()}'")
                        except ValueError:
                            raise DataFileSyntaxError(f"'{field.strip()}'")
                DS.__AddChapter(chpt)
        except FileNotFoundError:
            raise DataFileNotFoundError()

        else:
            DS.__isLoaded = True
            DS.__path_to_file = path_to_file
            DS.Log("Файл загружен успешно")

    @staticmethod
    def Save(path_to_file: str = ""):
        DS.__CheckWordload()
        DS.Log(f"Попытка сохранить файл в '{path_to_file}'")
        path_to_file = DS.__path_to_file if path_to_file.strip() == "" else path_to_file
        with open(path_to_file, "w") as file:
            for chapter in DS.__chapters:
                file.write(f"# {chapter.name} " + "{\n")
                for field in chapter.fields:
                    file.write("    " + str(field) + "\n")
                file.write("}\n\n")
        DS.Log("Сохранено успешно")

    @staticmethod
    def DeleteChapter(chapter_name: str):
        DS.__CheckWordload()
        DS.Log(f"Удаление раздела '{chapter_name}'...")
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                DS.__chapters.remove(chapter)
                DS.Log(f"Раздел '{chapter.name} удалён'")
                return
        raise ChapterNotExistError()

    @staticmethod
    def DeleteField(chapter_name: str, field_name: str):
        DS.__CheckWordload()
        DS.Log(f"Удаление поля '{field_name}'...")
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        chapter.fields.remove(field)
                        DS.Log(f"Поле '{field.name}' удалено")
                        return
                raise FieldNotExistError()
        raise ChapterNotExistError()

    @staticmethod
    def SetField(chapter_name: str, field_name: str, value: any, CreateIfNotExist=False):
        DS.__CheckWordload()
        DS.Log(f"Установка нового значения для поля '{field_name}'...")
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        field.value = str(value)
                        DS.Log(f"Установлено новое значение для поля '{field.name}': '{field.value}'")
                        return
                if CreateIfNotExist:
                    DS.Log(f"При попытке установить новое значение, не было найдено поле '{field_name}'")
                    DS.CreateField(chapter_name, field_name, value)
                    return
                else:
                    raise FieldNotExistError()
            if CreateIfNotExist:
                DS.Log(f"При попытке установить новое значение, не был найден раздел '{chapter_name}'")
                DS.CreateChapter(chapter_name)
                DS.CreateField(chapter_name, field_name, value)
                return
        raise ChapterNotExistError()

    @staticmethod
    def CreateChapter(chapter_name: str):
        DS.__CheckWordload()
        DS.Log(f"Создание нового раздела с именем '{chapter_name}'")
        DS.__CheckName(chapter_name)
        DS.__AddChapter(Chapter(chapter_name))
        DS.Log(f"Добавлен новый раздел с именем '{chapter_name}'")

    @staticmethod
    def CreateField(chapter_name: str, field_name: str, value=""):
        DS.__CheckWordload()
        DS.Log(f"Создание нового поля с именем '{field_name}'...")
        DS.__CheckName(field_name)
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                chapter.Add(field_name, value)
                DS.Log(f"Добавлено новое поле с именем '{field_name}' в разделе '{chapter_name}'")
                return
        raise ChapterNotExistError()

    @staticmethod
    def RenameChapter(old_chapter_name: str, new_chapter_name):
        DS.__CheckWordload()
        DS.Log(f"Переименование раздела '{old_chapter_name}'...")
        DS.__CheckName(new_chapter_name)
        for chapter in DS.__chapters:
            if chapter.name == old_chapter_name:
                chapter.name = new_chapter_name
                DS.Log(f"Раздел '{old_chapter_name}' был переименован на '{new_chapter_name}'")
                return
        raise ChapterNotExistError()

    @staticmethod
    def RenameField(chapter_name: str, old_field_name: str, new_field_name: str):
        DS.__CheckWordload()
        DS.Log(f"Переименование поля '{old_field_name}'...")
        DS.__CheckName(old_field_name)
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == old_field_name:
                        field.name = new_field_name
                        DS.Log(f"Поле '{old_field_name}' было переименовано на '{new_field_name}'")
                        return
                raise FieldNotExistError()
        raise ChapterNotExistError()

    @staticmethod
    def GetFieldValue(chapter_name: str, field_name: str) -> str:
        DS.__CheckWordload()
        DS.Log(f"Получение значения из поля '{field_name}'")
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        DS.Log(f"Получено значение из поля '{field.name}'")
                        return field.value
                raise FieldNotExistError()
        raise ChapterNotExistError()
