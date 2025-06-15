# manimlib/mobject/functions.py 详解

## 1. 类结构与关键属性（PlantUML类图）

```plantuml
@startuml
class VMobject {
}

class ParametricCurve {
  - t_func: Callable[[float], Sequence[float] | Vect3]
  - t_range: Tuple[float, float, float]
  - epsilon: float
  - discontinuities: Sequence[float]
  - use_smoothing: bool
  + get_point_from_function(t: float): Vect3
  + init_points()
  + get_t_func()
  + get_function()
  + get_x_range()
}

class FunctionGraph {
  - function: Callable[[float], float]
  - x_range: Tuple[float, float, float]
}

class ImplicitFunction {
  - func: Callable[[float, float], float]
  - x_range: Tuple[float, float]
  - y_range: Tuple[float, float]
  - min_depth: int
  - max_quads: int
  - use_smoothing: bool
  - joint_type: str
}

VMobject <|-- ParametricCurve
ParametricCurve <|-- FunctionGraph
VMobject <|-- ImplicitFunction
@enduml
```

### 关键属性说明
- `t_func`：参数方程，输入t返回空间点（支持2D/3D）。
- `t_range`：参数t的取值范围与步长。
- `epsilon`：处理不连续点时的微小偏移。
- `discontinuities`：参数区间内的断点集合。
- `use_smoothing`：是否对曲线进行平滑处理。
- `function`：一元函数，FunctionGraph专用。
- `x_range`：FunctionGraph的自变量范围。
- `func`：隐式函数，ImplicitFunction专用。
- `x_range, y_range`：隐式函数的自变量范围。
- `min_depth, max_quads`：等值线绘制的递归深度与最大分块数。
- `joint_type`：曲线连接方式。

## 2. 关键方法与算法（PlantUML时序图）

### 2.1 ParametricCurve.init_points()

```plantuml
@startuml
actor User
participant ParametricCurve
participant numpy as np
User -> ParametricCurve: init_points()
ParametricCurve -> ParametricCurve: 解析t_range, discontinuities
ParametricCurve -> np: 生成分段区间
loop 每个区间
  ParametricCurve -> ParametricCurve: 采样t, 计算点集
  ParametricCurve -> ParametricCurve: start_new_path()
  ParametricCurve -> ParametricCurve: add_points_as_corners()
end
alt use_smoothing
  ParametricCurve -> ParametricCurve: make_smooth(approx=True)
end
alt 没有点
  ParametricCurve -> ParametricCurve: set_points()
end
@enduml
```

#### 关键算法说明
- 断点处理：将参数区间按discontinuities分段，避免在不连续点处连线。
- 采样：对每个分段区间，按步长采样，生成点集。
- 平滑：可选，对采样点做平滑处理。

### 2.2 ImplicitFunction.__init__

```plantuml
@startuml
actor User
participant ImplicitFunction
participant plot_isoline
User -> ImplicitFunction: __init__()
ImplicitFunction -> plot_isoline: 计算等值线
plot_isoline --> ImplicitFunction: 返回曲线点集
loop 每条曲线
  ImplicitFunction -> ImplicitFunction: start_new_path()
  ImplicitFunction -> ImplicitFunction: add_points_as_corners()
end
alt use_smoothing
  ImplicitFunction -> ImplicitFunction: make_smooth()
end
@enduml
```

#### 关键算法说明
- plot_isoline：对隐式函数f(x, y)=0进行等值线追踪，返回曲线点集。
- 曲线拼接：每条等值线作为一条路径加入VMobject。

## 3. 使用方法与示例

### 3.1 ParametricCurve 示例
```python
from manimlib.mobject.functions import ParametricCurve
import numpy as np

# 绘制螺旋线
curve = ParametricCurve(
    t_func=lambda t: [np.cos(t), np.sin(t), t/10],
    t_range=(0, 4 * np.pi, 0.05),
    color="BLUE"
)
```

### 3.2 FunctionGraph 示例
```python
from manimlib.mobject.functions import FunctionGraph

# 绘制y=sin(x)曲线
graph = FunctionGraph(
    function=lambda x: np.sin(x),
    x_range=(-3.14, 3.14, 0.05),
    color="YELLOW"
)
```

### 3.3 ImplicitFunction 示例
```python
from manimlib.mobject.functions import ImplicitFunction

# 绘制单位圆x^2 + y^2 = 1
implicit = ImplicitFunction(
    func=lambda x, y: x**2 + y**2 - 1,
    x_range=(-2, 2),
    y_range=(-2, 2),
    color="GREEN"
)
```

## 4. 总结
- `ParametricCurve`适合任意参数曲线，支持断点与平滑。
- `FunctionGraph`专为y=f(x)设计，简化常见函数曲线绘制。
- `ImplicitFunction`可绘制任意隐式曲线，适合复杂边界。
- 三者均继承自`VMobject`，可与manim动画系统无缝集成。
