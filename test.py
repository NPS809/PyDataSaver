from DataSaver import *

DS.Load("data.dat")

value = DS.GetFieldValue("GGG", "name1")
print(f"Value: {value}")

DS.Save("data.dat")

print("Тест завершён")
