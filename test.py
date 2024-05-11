import time

from DataSaver import *

input("Тестирование системы сохранения данных.\nНажмите enter, чтобы начать")
start_time = time.time()
DS.EnableLogs()

DS.Load("data.dat")

DS.CreateChapter("new_chapter")

DS.CreateField("new_chapter", "new_field")

DS.SetField("new_chapter", "new_field", "new_value")

DS.SetField("dehfe", "hgure", "ghruehjgrte", True)

DS.RenameChapter("new_chapter", "new_New_chapter")

DS.RenameField("dehfe", "hgure", "field")

DS.DeleteField("new_main_chapter", "field")

DS.DeleteChapter("dehfe")

DS.Save("new_data.dat")
end_time = time.time() - start_time
print("Тест завершён")
time.sleep(1)
print(f'Время выполнения: {round(end_time, 2)}s')
input()
