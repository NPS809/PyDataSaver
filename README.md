

# DataSaver
### maybe, such as json, but!!! much simpler

This is a simple data saver using python.
Now, this doesnt have any ui, but you can use code.

## Base functions:

```python
from DataSaver import DS

DS.Load("path_to_data_file.dat")
```
This code will be load all data.

Data file syntax:
```
# ChapterName {
    field_name1 : field_value
}
```

Also, you can save data file

```python
from DataSaver import DS

# it will be save in new file
DS.Save("path_to_new_data_file")

# it will be save in same file
DS.Save()
```

## Actions with Chapters and Fields

You can delete Chapters and Fields:

```python
from DataSaver import DS

DS.DeleteChapter("chapter_name")
# If chapter is not exits, it will be raise ChapterNotExist error
# similarly with fields
DS.DeleteField("chapter_name", "field_name")
```

You can add your own Chapters and Fields:

```python
from DataSaver import DS

DS.CreateChapter("new_chapter_name")
# If chapter exist, it will be raise error
# similalry with fields
DS.CreateField("chapter_name", "field_name", "value")
```

You can sets value for exist field:

```python
from DataSaver import DS

DS.SetField("chapter_name", "field_name", "value")
# Also, it has CreateIfNotExist argument
# if field not exist, it will create new
DS.SetField("chapter_name", "field_name", "value", CreateIfNotExist=True)
```

You can rename Chapters and Fields:

```python
from DataSaver import DS

DS.RenameChapter("old_chapter_name", "new_chapter_name")
DS.RenameField("chapter_name", "old_field_name", "new_field_name")
```

