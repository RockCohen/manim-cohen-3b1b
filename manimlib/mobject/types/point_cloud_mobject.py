from __future__ import annotations

import numpy as np

from manimlib.mobject.mobject import Mobject
from manimlib.utils.color import color_gradient
from manimlib.utils.color import color_to_rgba
from manimlib.utils.iterables import resize_with_interpolation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import ManimColor, Vect3, Vect3Array, Vect4Array, Self
# PMobject 是 Manim 库中用于表示“点云对象”（Point Cloud Mobject）的类。
# 它继承自 Mobject，是所有基于点的可视化对象的基础类。其含义和作用如下：
# 含义: P 代表 Point（点），PMobject 即 Point Cloud Mobject，意为“点云对象”。
# 它是所有由一组点（point cloud）组成的对象的基类，比如 DotCloud、VMobject（矢量图形对象）等。
# 作用
# 管理点数据：PMobject 主要负责存储和操作一组三维点（通常是 N×3 的 numpy 数组），以及与每个点相关的颜色（rgba）等属性。
# 点的增删改查：提供了如 set_points、add_points、add_point 等方法，方便地设置、添加、操作点。
# 颜色与透明度控制：可以通过 set_color_by_gradient、match_colors 等方法为点设置渐变色或匹配其他对象的颜色。
# 点的排序与筛选：如 sort_points、filter_out 方法，可以根据自定义函数对点进行排序或筛选。
# 子对象合并：ingest_submobjects 方法可以将所有子 PMobject 的点合并到当前对象中。
# 动画支持：如 pointwise_become_partial 支持动画中部分点的变换。
# 典型应用
# 任何需要以“点”为基本单元进行动画或可视化的对象，都可以基于 PMobject 实现。例如，绘制散点图、粒子动画、路径采样等。

class PMobject(Mobject):
    def set_points(self, points: Vect3Array):
        if len(points) == 0:
            points = np.zeros((0, 3))
        super().set_points(points)
        self.resize_points(len(points))
        return self

    def add_points(
        self,
        points: Vect3Array,
        rgbas: Vect4Array | None = None,
        color: ManimColor | None = None,
        opacity: float | None = None
    ) -> Self:
        """
        points must be a Nx3 numpy array, as must rgbas if it is not None
        """
        self.append_points(points)
        # rgbas array will have been resized with points
        if color is not None:
            if opacity is None:
                opacity = self.data["rgba"][-1, 3]
            rgbas = np.repeat(
                [color_to_rgba(color, opacity)],
                len(points),
                axis=0
            )
        if rgbas is not None:
            self.data["rgba"][-len(rgbas):] = rgbas
        return self

    def add_point(self, point: Vect3, rgba=None, color=None, opacity=None) -> Self:
        rgbas = None if rgba is None else [rgba]
        self.add_points([point], rgbas, color, opacity)
        return self

    @Mobject.affects_data
    def set_color_by_gradient(self, *colors: ManimColor) -> Self:
        self.data["rgba"][:] = np.array(list(map(
            color_to_rgba,
            color_gradient(colors, self.get_num_points())
        )))
        return self

    @Mobject.affects_data
    def match_colors(self, pmobject: PMobject) -> Self:
        self.data["rgba"][:] = resize_with_interpolation(
            pmobject.data["rgba"], self.get_num_points()
        )
        return self

    @Mobject.affects_data
    def filter_out(self, condition: Callable[[np.ndarray], bool]) -> Self:
        for mob in self.family_members_with_points():
            mob.data = mob.data[~np.apply_along_axis(condition, 1, mob.get_points())]
        return self

    @Mobject.affects_data
    def sort_points(self, function: Callable[[Vect3], None] = lambda p: p[0]) -> Self:
        """
        function is any map from R^3 to R
        """
        for mob in self.family_members_with_points():
            indices = np.argsort(
                np.apply_along_axis(function, 1, mob.get_points())
            )
            mob.data[:] = mob.data[indices]
        return self

    @Mobject.affects_data
    def ingest_submobjects(self) -> Self:
        self.data = np.vstack([
            sm.data for sm in self.get_family()
        ])
        return self

    def point_from_proportion(self, alpha: float) -> np.ndarray:
        index = alpha * (self.get_num_points() - 1)
        return self.get_points()[int(index)]

    @Mobject.affects_data
    def pointwise_become_partial(self, pmobject: PMobject, a: float, b: float) -> Self:
        lower_index = int(a * pmobject.get_num_points())
        upper_index = int(b * pmobject.get_num_points())
        self.data = pmobject.data[lower_index:upper_index].copy()
        return self


class PGroup(PMobject):
    def __init__(self, *pmobs: PMobject, **kwargs):
        if not all([isinstance(m, PMobject) for m in pmobs]):
            raise Exception("All submobjects must be of type PMobject")
        super().__init__(**kwargs)
        self.add(*pmobs)
