# CColorPicker

[使用方法](/TestCColorPicker.py)

```python
from CColorPicker.CColorPicker import CColorPicker

ret, color = CColorPicker.getColor()
if ret == CColorPicker.Accepted:
    print(color.name())
```

![CColorPicker](/ScreenShot/CColorPicker.gif)