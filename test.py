from DataSaver import *

DS.Load("data.dat")

DS.RenameChapter("GGG", "first_chapter")
DS.RenameField("GGG2", "name4", "new_Field_name")

DS.Save("new_data.dat")
print("Тест заверщён")
