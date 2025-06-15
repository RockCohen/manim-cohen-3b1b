# manimlib.mobject.probability 源码解析

## 1. 类结构与关键属性（PlantUML 类图）

```plantuml
@startuml
class SampleSpace {
  +float width
  +float height
  +ManimColor fill_color
  +float fill_opacity
  +float stroke_width
  +ManimColor stroke_color
  +float default_label_scale_val
  +VGroup horizontal_parts
  +VGroup vertical_parts
  +TexText title
  +str label
  +VGroup braces
  +VGroup labels
  +dict label_kwargs
  +add_title(title, buff)
  +add_label(label)
  +divide_horizontally(...)
  +divide_vertically(...)
  +get_horizontal_division(...)
  +get_vertical_division(...)
  +get_subdivision_braces_and_labels(...)
  +add_braces_and_labels()
}

class BarChart {
  +float height
  +float width
  +int n_ticks
  +bool include_x_ticks
  +float tick_width
  +float tick_height
  +bool label_y_axis
  +float y_axis_label_height
  +float max_value
  +list bar_colors
  +float bar_fill_opacity
  +float bar_stroke_width
  +list bar_names
  +float bar_label_scale_val
  +VGroup bars
  +VGroup bar_labels
  +add_axes()
  +add_bars(values)
  +change_bar_values(values)
}

SampleSpace <|-- Rectangle
BarChart <|-- VGroup
@enduml
```

### 关键属性说明
- `SampleSpace`
  - `width`, `height`：样本空间矩形的宽高。
  - `fill_color`, `fill_opacity`：填充色及透明度。
  - `stroke_width`, `stroke_color`：边框宽度与颜色。
  - `default_label_scale_val`：标签缩放比例。
  - `horizontal_parts`, `vertical_parts`：水平/垂直分割后的子区域（VGroup）。
  - `title`, `label`：标题与标签。
  - `braces`, `labels`, `label_kwargs`：分割后括号与标签及其参数。

- `BarChart`
  - `height`, `width`：图表整体高宽。
  - `n_ticks`：y轴刻度数。
  - `include_x_ticks`：是否包含x轴刻度。
  - `tick_width`, `tick_height`：刻度线宽高。
  - `label_y_axis`：是否显示y轴标签。
  - `y_axis_label_height`：y轴标签高度。
  - `max_value`：y轴最大值。
  - `bar_colors`：柱状条颜色列表。
  - `bar_fill_opacity`：柱状条填充透明度。
  - `bar_stroke_width`：柱状条边框宽度。
  - `bar_names`：每个柱状条的名称。
  - `bar_label_scale_val`：柱状条标签缩放比例。
  - `bars`, `bar_labels`：柱状条及其标签（VGroup）。


## 2. 关键方法与算法实现（PlantUML 时序图）

### 2.1 SampleSpace 分割与标注

#### 水平/垂直分割
```plantuml
@startuml
actor User
participant SampleSpace
participant VGroup
User -> SampleSpace: divide_horizontally(p_list, ...)
SampleSpace -> SampleSpace: get_horizontal_division(p_list, ...)
SampleSpace -> SampleSpace: get_division_along_dimension(p_list, dim=1, ...)
SampleSpace -> VGroup: 创建分割区域
SampleSpace -> SampleSpace: 添加horizontal_parts
@enduml
```

#### 添加分割括号与标签
```plantuml
@startuml
actor User
participant SampleSpace
participant VGroup
User -> SampleSpace: get_side_braces_and_labels(labels, ...)
SampleSpace -> SampleSpace: get_subdivision_braces_and_labels(parts, labels, ...)
SampleSpace -> VGroup: 为每个分区创建Brace和Tex标签
SampleSpace -> SampleSpace: 返回VGroup(Braces, Labels)
@enduml
```

### 2.2 BarChart 柱状图生成

```plantuml
@startuml
actor User
participant BarChart
participant VGroup
User -> BarChart: __init__(values, ...)
BarChart -> BarChart: add_axes()
BarChart -> BarChart: add_bars(values)
BarChart -> VGroup: 创建每个柱状条和标签
BarChart -> BarChart: 组合并居中
@enduml
```


## 3. 用法示例

### 3.1 SampleSpace 示例
```python
from manimlib.mobject.probability import SampleSpace
from manimlib.constants import GREEN_E, BLUE_E

# 创建样本空间
ss = SampleSpace(width=4, height=2)
ss.add_title("样本空间示例")
ss.divide_horizontally([0.3, 0.7], colors=[GREEN_E, BLUE_E])
ss.get_side_braces_and_labels(["A", "B"])
ss.add_braces_and_labels()
```

### 3.2 BarChart 示例
```python
from manimlib.mobject.probability import BarChart

values = [0.2, 0.5, 0.3]
names = ["A", "B", "C"]
chart = BarChart(values, bar_names=names, bar_colors=["#3498db", "#e67e22", "#2ecc71"])
```


## 4. 总结与建议

### SampleSpace
- **使用场景**：概率论、统计学动画中用于展示样本空间及其分割、标注。
- **特性**：支持灵活的水平/垂直分割，自动补全概率分布，支持分区括号与标签。
- **建议**：
  - 分割比例之和不为1时会自动补全，注意概率分布的合理性。
  - 分割后可通过`get_side_braces_and_labels`等方法添加分区说明。
  - 适合与动画结合，展示事件、条件概率等。

### BarChart
- **使用场景**：用于概率分布、频率分布等柱状图可视化。
- **特性**：支持自定义颜色、标签、y轴刻度，动态调整柱状条高度。
- **建议**：
  - `bar_names`与`values`长度需一致。
  - 可通过`change_bar_values`动态更新数据。
  - 适合用于概率、统计、数据可视化等场景。

---

> 本文档由AI自动生成，建议结合实际代码进一步理解和扩展。
