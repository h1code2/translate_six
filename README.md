## translate_six
A simple package based on the google translation interface

**example:**
```python
from translate import Translate

result = Translate.start_translate("hello")

print(result) # Return a string

result = Translate.start_translate("like you\npeople")

print(result) # Return an list
```