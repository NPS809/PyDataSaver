class Field:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name} : {self.value}"


class Chapter:
    def __init__(self, name: str):
        self.name = name
        self.fields: list[Field] = []

    def Add(self, name: str, value: str):
        for field in self.fields:
            if name.strip() == field.name:
                print("Ячейка с таким именем уже существует!")
                return
        self.fields.append(Field(name.strip(), value.strip()))

    def __str__(self):
        text = f"{self.name} " + "{\n"
        for field in self.fields:
            text += "   " + str(field) + "\n"
        text += "}"
        return text
