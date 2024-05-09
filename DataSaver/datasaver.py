from string import ascii_letters
from DataSaver.errors import *
from DataSaver.classes import *

available_chars = ["a", "b", "c", "d", "e", "f", "g", "h", "j", "i", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                   "u", "w", "v", "x", "y", "z",
                   "A", "B", "C", "D", "E", "F", "G", "H", "J", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "U", "W", "V", "X", "Y", "Z",
                   "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", " ", "_"]


class DS:
    isLoaded: bool = False
    path_to_file: str = ""
    chapters: list[Chapter] = []

    @staticmethod
    def CheckName(name: str):
        if not name:
            raise IncorrectNameError(name)
        for char in name:
            if char not in available_chars:
                raise IncorrectNameError(name)

    @staticmethod
    def AddChapter(chapter: Chapter):
        if chapter in DS.chapters:
            raise ChapterAlreadyExistError()
        DS.chapters.append(chapter)

    @staticmethod
    def CheckWordload():
        if not DS.isLoaded:
            raise DataFileNotLoadedError()

    @staticmethod
    def Load(path_to_file: str):
        try:
            with open(path_to_file, "r") as file:
                strings = file.readlines()
                chapters = []
                for i in range(len(strings)):
                    if "#" in strings[i]:
                        for j in range(i, len(strings)):
                            if "}" in strings[j]:
                                chapters.append([i, j])
                                break
                chapters = [strings[a:b] for a, b in chapters]

                for chapter in chapters:
                    chpt_name = chapter[0]
                    chpt_name = chpt_name.strip()
                    chpt_name = chpt_name.removeprefix("#")
                    chpt_name = chpt_name.removesuffix("{")
                    chpt_name = chpt_name.strip()

                    DS.CheckName(chpt_name)
                    chpt = Chapter(chpt_name)

                    for string in chapter[1:]:
                        try:
                            name, value = string.split(":")
                            name = name.strip()
                            value = value.strip()
                            DS.CheckName(name)
                            chpt.Add(name, value)
                        except SyntaxError:
                            raise DataFileSyntaxError(string)
                        except TypeError:
                            raise DataFileSyntaxError(f"'{string.strip()}'")

                    DS.AddChapter(chpt)
        except FileNotFoundError:
            raise DataFileNotFoundError()

        else:
            DS.isLoaded = True
            DS.path_to_file = path_to_file

    @staticmethod
    def Save(path_to_file: str = ""):
        DS.CheckWordload()
        path_to_file = DS.path_to_file if path_to_file.strip() == "" else path_to_file

        with open(path_to_file, "w") as file:
            for chapter in DS.chapters:
                file.write(f"# {chapter.name} " + "{\n")
                for field in chapter.fields:
                    file.write("    " + str(field) + "\n")
                file.write("}\n\n")

    @staticmethod
    def DeleteChapter(chapter_name: str):
        DS.CheckWordload()
        for chapter in DS.chapters:
            if chapter.name == chapter_name:
                DS.chapters.remove(chapter)
                return
        raise ChapterNotExistError()

    @staticmethod
    def DeleteField(chapter_name: str, field_name: str):
        DS.CheckWordload()
        for chapter in DS.chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        chapter.fields.remove(field)
                        return
                raise FieldNotExistError()
        raise ChapterNotExistError()

    @staticmethod
    def SetField(chapter_name: str, field_name: str, value: any, CreateIfNotExist=False):
        DS.CheckWordload()
        for chapter in DS.chapters:
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
        raise ChapterNotExistError()

    @staticmethod
    def CreateChapter(chapter_name: str):
        DS.CheckWordload()
        DS.CheckName(chapter_name)
        DS.AddChapter(Chapter(chapter_name))

    @staticmethod
    def CreateField(chapter_name: str, field_name: str, value=""):
        DS.CheckWordload()
        DS.CheckName(field_name)
        for chapter in DS.chapters:
            if chapter.name == chapter_name:
                chapter.Add(field_name, value)
                return
        raise ChapterNotExistError()

    @staticmethod
    def RenameChapter(old_chapter_name: str, new_chapter_name):
        DS.CheckWordload()
        DS.CheckName(new_chapter_name)
        for chapter in DS.chapters:
            if chapter.name == old_chapter_name:
                chapter.name = new_chapter_name
                return
        raise ChapterNotExistError()

    @staticmethod
    def RenameField(chapter_name: str, old_field_name: str, new_field_name: str):
        DS.CheckWordload()
        DS.CheckName(old_field_name)
        for chapter in DS.chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == old_field_name:
                        field.name = new_field_name
                        return
                raise FieldNotExistError()
        raise ChapterNotExistError()
