import re
from string import ascii_letters
from DataSaver.errors import *
from DataSaver.classes import *


class DS:
    __isLoaded: bool = False
    __path_to_file: str = ""
    __chapters: list[Chapter] = []
    __av_chars = list(ascii_letters) + ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ", "_"]

    @staticmethod
    def __CheckName(name: str):
        """DataSaver private method"""
        if not name:
            raise IncorrectNameError(name)
        for char in name:
            if char not in DS.__av_chars:
                raise IncorrectNameError(name)

    @staticmethod
    def __AddChapter(chapter: Chapter):
        """DataSaver private method"""
        if chapter in DS.__chapters:
            raise ChapterAlreadyExistError()
        DS.__chapters.append(chapter)

    @staticmethod
    def __CheckWordload():
        """DataSaver private method"""
        if not DS.__isLoaded:
            raise DataFileNotLoadedError()

    @staticmethod
    def Load(path_to_file: str):
        try:
            with open(path_to_file, "r", encoding="utf-8") as file:
                lines = file.read()

            while " " in lines:
                lines = lines.replace(" ", "")
            while "\n" in lines:
                lines = lines.replace("\n", "")

            chapters = []
            pattern = r'#"(.*?)"{(.*?)}'

            matches = re.findall(pattern, lines)

            for match in matches:
                chapter_name = match[0]
                fields_str = match[1]

                chapter = Chapter(chapter_name)
                fields = fields_str.split(',')

                for field in fields:
                    if field.replace(" ", ""):
                        try:
                            key, value = field.split(':')
                            chapter.Add(key.strip('"'), value.strip('"'))
                        except Exception as ex:
                            raise DataFileSyntaxError(field)

                chapters.append(chapter)
        except FileNotFoundError:
            raise DataFileNotFoundError()

        else:
            DS.__isLoaded = True
            DS.__path_to_file = path_to_file

    @staticmethod
    def Save(path_to_file: str = ""):
        DS.__CheckWordload()
        path_to_file = DS.__path_to_file if path_to_file.strip() == "" else path_to_file
        with open(path_to_file, "w") as file:
            for chapter in DS.__chapters:
                file.write(f"# {chapter.name} " + "{\n")
                for field in chapter.fields:
                    file.write("    " + str(field) + "\n")
                file.write("}\n\n")

    @staticmethod
    def DeleteChapter(chapter_name: str):
        DS.__CheckWordload()
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                DS.__chapters.remove(chapter)
                return
        raise ChapterNotExistError()

    @staticmethod
    def DeleteField(chapter_name: str, field_name: str):
        DS.__CheckWordload()
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        chapter.fields.remove(field)
                        return
                raise FieldNotExistError()
        raise ChapterNotExistError()

    @staticmethod
    def SetField(chapter_name: str, field_name: str, value: any, CreateIfNotExist=False):
        DS.__CheckWordload()
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        field.value = str(value)
                        return
                if CreateIfNotExist:
                    DS.CreateField(chapter_name, field_name, value)
                    return
                else:
                    raise FieldNotExistError()
            if CreateIfNotExist:
                DS.CreateChapter(chapter_name)
                DS.CreateField(chapter_name, field_name, value)
                return
        raise ChapterNotExistError()

    @staticmethod
    def CreateChapter(chapter_name: str):
        DS.__CheckWordload()
        DS.__CheckName(chapter_name)
        DS.__AddChapter(Chapter(chapter_name))

    @staticmethod
    def CreateField(chapter_name: str, field_name: str, value=""):
        DS.__CheckWordload()
        DS.__CheckName(field_name)
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                chapter.Add(field_name, value)
                return
        raise ChapterNotExistError()

    @staticmethod
    def RenameChapter(old_chapter_name: str, new_chapter_name):
        DS.__CheckWordload()
        DS.__CheckName(new_chapter_name)
        for chapter in DS.__chapters:
            if chapter.name == old_chapter_name:
                chapter.name = new_chapter_name
                return
        raise ChapterNotExistError()

    @staticmethod
    def RenameField(chapter_name: str, old_field_name: str, new_field_name: str):
        DS.__CheckWordload()
        DS.__CheckName(old_field_name)
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == old_field_name:
                        field.name = new_field_name
                        return
                raise FieldNotExistError()
        raise ChapterNotExistError()

    @staticmethod
    def GetFieldValue(chapter_name: str, field_name: str) -> str:
        DS.__CheckWordload()
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        return field.value
                raise FieldNotExistError()
        raise ChapterNotExistError()

    @staticmethod
    def isField(chapter_name: str, field_name: str) -> bool:
        DS.__CheckWordload()
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        return True
        return False

    @staticmethod
    def isChapter(chapter_name) -> bool:
        DS.__CheckWordload()
        for chapter in DS.__chapters:
            if chapter.name == chapter_name:
                return True
        return False
