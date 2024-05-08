

# DataSaver
### maybe, such as json, but!!! much simplier

This is a simple data saver using python.
Now, this doesnt have any ui, but you can use code.

Now, you can use next functions:

```python
from datasaver import *
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
from datasaver import *

# it will be save in new file
DS.Save("path_to_new_data_file")

# it will be save in same file
DS.Save()
```