from DataSaver import DS

DS.Load("data.dat")

DS.CreateChapter("New Test Chapter")
DS.SetField("New Test Chapter", "name", "value", True)
DS.CreateField("New Test Chapter", "new_field", "any value")

DS.Save("new_data.dat")
print("Тест завершён")
