# manimlib.mobject.svg.brace 源码详解

## 1. 类及关键属性介绍（PlantUML类图）

本文件主要包含以下类：

- `Brace`
- `BraceLabel`
- `BraceText`
- `LineBrace`

### 主要类关系与属性说明

```plantuml
@startuml
class Tex {
}

class VMobject {
}

class Brace {
  - tip_point_index: int
  + set_initial_width(width: float)
  + put_at_tip(mob, use_next_to=True, **kwargs)
  + get_text(text: str, **kwargs): Text
  + get_tex(*tex: str, **kwargs): Tex
  + get_tip(): np.ndarray
  + get_direction(): np.ndarray
}

class BraceLabel {
  - brace_direction: np.ndarray
  - label_scale: float
  - label_buff: float
  - brace: Brace
  - label: Tex
  + creation_anim(label_anim=FadeIn, brace_anim=GrowFromCenter): AnimationGroup
  + shift_brace(obj, **kwargs)
  + change_label(*text, **kwargs)
  + change_brace_label(obj, *text)
  + copy()
}

class BraceText {
}

class LineBrace {
}

Tex <|-- Brace
VMobject <|-- BraceLabel
BraceLabel <|-- BraceText
Brace <|-- LineBrace
@enduml
```

#### 关键属性说明

- `Brace`
  - `tip_point_index`: 括号尖端在点集中的索引，用于定位括号的“尖”。
- `BraceLabel`
  - `brace_direction`: 括号朝向（如DOWN、UP等）。
  - `label_scale`: 标签缩放比例。
  - `label_buff`: 标签与括号的间距。
  - `brace`: 关联的`Brace`对象。
  - `label`: 关联的标签对象（如Tex/Text）。
- `BraceText`
  - 继承自`BraceLabel`，其`label_constructor`为`TexText`。
- `LineBrace`
  - 继承自`Brace`，用于与`Line`对象配合，自动适应线段方向。

---

## 2. 关键方法与算法详解（PlantUML时序图）

### Brace的构造与对齐

```plantuml
@startuml
actor User
participant "Brace.__init__" as BraceInit
participant "Tex.__init__" as TexInit
participant "mobject.rotate"
participant "self.get_all_points"
participant "self.set_initial_width"
participant "self.shift"
participant "mob.rotate"

User -> BraceInit: 创建Brace(mobject, direction, ...)
BraceInit -> TexInit: super().__init__(tex_string, ...)
BraceInit -> mobject.rotate: 旋转mobject以对齐方向
BraceInit -> mobject.get_corner: 获取左下/右下角
BraceInit -> self.get_all_points: 获取所有点
BraceInit -> self.set_initial_width: 设置括号宽度
BraceInit -> self.shift: 移动括号到目标位置
loop 恢复原始角度
    BraceInit -> mob.rotate: 旋转回去
end
@enduml
```

### BraceLabel的创建与标签放置

```plantuml
@startuml
actor User
participant "BraceLabel.__init__" as BLInit
participant "Brace"
participant "label_constructor"
participant "label.scale"
participant "brace.put_at_tip"
participant "self.set_submobjects"

User -> BLInit: 创建BraceLabel(obj, text, ...)
BLInit -> Brace: 创建Brace
BLInit -> label_constructor: 创建label
BLInit -> label.scale: 缩放label
BLInit -> brace.put_at_tip: 放置label到括号尖端
BLInit -> self.set_submobjects: 设置子对象
@enduml
```

### Brace的put_at_tip方法

```plantuml
@startuml
actor User
participant "Brace.put_at_tip"
participant "mob.next_to"
participant "mob.move_to"
participant "mob.shift"

User -> "Brace.put_at_tip": 调用put_at_tip(mob, use_next_to, ...)
alt use_next_to为True
    "Brace.put_at_tip" -> "mob.next_to": 放置到括号尖端
else
    "Brace.put_at_tip" -> "mob.move_to": 移动到尖端
    "Brace.put_at_tip" -> "mob.shift": 按方向偏移
end
@enduml
```

---

## 3. 使用方法与高质量代码示例

### 示例1：为矩形添加括号与标签

```python
from manimlib import *

class BraceExample(Scene):
    def construct(self):
        rect = Rectangle(width=4, height=2)
        brace = Brace(rect, DOWN)
        label = brace.get_text("宽度")
        self.add(rect, brace, label)
        self.wait()
```

### 示例2：使用BraceLabel自动管理括号与标签

```python
from manimlib import *

class BraceLabelExample(Scene):
    def construct(self):
        rect = Rectangle(width=4, height=2)
        brace_label = BraceLabel(rect, "宽度", brace_direction=DOWN)
        self.add(rect, brace_label)
        self.wait()
```

### 示例3：动态改变括号和标签

```python
from manimlib import *

class DynamicBraceLabel(Scene):
    def construct(self):
        rect1 = Rectangle(width=4, height=2)
        rect2 = Rectangle(width=2, height=2).shift(RIGHT*3)
        brace_label = BraceLabel(rect1, "A", brace_direction=DOWN)
        self.add(rect1, rect2, brace_label)
        self.wait()
        # 改变括号和标签
        self.play(
            Transform(brace_label, brace_label.change_brace_label(rect2, "B"))
        )
        self.wait()
```

### 示例4：LineBrace的用法

```python
from manimlib import *

class LineBraceExample(Scene):
    def construct(self):
        line = Line(LEFT, RIGHT)
        brace = LineBrace(line, UP)
        self.add(line, brace)
        self.wait()
```

---

## 4. 备注

- `Line`、`TexText`等依赖需确保manimlib环境完整。
- 本文档适用于manimlib分支，部分API与社区版manim略有差异。
