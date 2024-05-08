class Field:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}:{self.value}"


class Chapter:
    def __init__(self, name: str):
        self.name = name
        self.fields: list[Field] = []

    def Add(self, name, value):
        for field in self.fields:
            if name == field.name:
                print("Ячейка с таким именем уже существует!")
                return
        self.fields.append(Field(name, value))

    def __str__(self):
        text = f"{self.name} " + "{\n"
        for field in self.fields:
            text += str(field)
        text += "}"
        return text


class DS:
    isLoaded: bool = False
    path_to_file: str = ""
    chapters: list[Chapter] = []

    @staticmethod
    def AddChapter(chapter: Chapter):
        if chapter not in DS.chapters:
            DS.chapters.append(chapter)
        else:
            print("Такой раздел уже существует!")

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
            print("Такого файла данных нет!")
        else:
            DS.path_to_file = path_to_file

    @staticmethod
    def Save(path_to_file: str = ""):
        if path_to_file.strip() == "":
            path_to_file = DS.path_to_file

        with open(path_to_file, "w") as file:
            for chapter in DS.chapters:
                file.write(f"# {chapter.name} " + "{\n")
                for field in chapter.fields:
                    file.write(str(field))
                file.write("}\n\n")


DS.Load("data.dat")
DS.Save("new_data.dat")
