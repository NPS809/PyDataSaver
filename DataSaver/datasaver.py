from DataSaver.errors import *
from DataSaver.classes import *


class DS:
    isLoaded: bool = False
    path_to_file: str = ""
    chapters: list[Chapter] = []

    @staticmethod
    def AddChapter(chapter: Chapter):
        if chapter in DS.chapters:
            raise ChapterAlreadyExist()
        DS.chapters.append(chapter)

    @staticmethod
    def CheckWordload():
        if not DS.isLoaded:
            raise DataFileNotLoaded()

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
                    chpt = Chapter(chapter[0].replace("#", "").replace("{", "").strip())
                    for string in chapter[1:]:
                        chpt.Add(*string.split(":"))
                    DS.AddChapter(chpt)
        except FileNotFoundError:
            raise DataFileNotFound()
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
        raise ChapterNotExist()

    @staticmethod
    def DeleteField(chapter_name: str, field_name: str):
        DS.CheckWordload()
        for chapter in DS.chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == field_name:
                        chapter.fields.remove(field)
                        return
                raise FieldNotExist()
        raise ChapterNotExist()

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
                    raise FieldNotExist()
        raise ChapterNotExist()

    @staticmethod
    def CreateChapter(chapter_name: str):
        DS.CheckWordload()
        DS.AddChapter(Chapter(chapter_name))

    @staticmethod
    def CreateField(chapter_name: str, field_name: str, value=""):
        DS.CheckWordload()
        for chapter in DS.chapters:
            if chapter.name == chapter_name:
                chapter.Add(field_name, value)
                return
        raise ChapterNotExist()

    @staticmethod
    def RenameChapter(old_chapter_name: str, new_chapter_name):
        DS.CheckWordload()
        for chapter in DS.chapters:
            if chapter.name == old_chapter_name:
                chapter.name = new_chapter_name
                return
        raise ChapterNotExist()

    @staticmethod
    def RenameField(chapter_name: str, old_field_name: str, new_field_name: str):
        DS.CheckWordload()
        for chapter in DS.chapters:
            if chapter.name == chapter_name:
                for field in chapter.fields:
                    if field.name == old_field_name:
                        field.name = new_field_name
                        return
                raise FieldNotExist()
        raise ChapterNotExist()
