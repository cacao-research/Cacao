"""
Chart components for Cacao v2.

Provides a simple API for creating interactive charts.

Example:
    from cacao.chart import line, bar, pie

    line(data, x="date", y="revenue", title="Revenue Over Time")
    bar(data, x="category", y="sales", title="Sales by Category")
    pie(data, values="amount", names="category", title="Distribution")
"""

from __future__ import annotations

from typing import Any, Literal
from dataclasses import dataclass, field

# Import from ui module to use same component system
from .ui import Component, _add_to_current_container


def _normalize_data(data: Any) -> list[dict[str, Any]]:
    """Convert various data formats to list of dicts."""
    # Pandas DataFrame
    if hasattr(data, 'to_dict'):
        return data.to_dict('records')
    # Already a list
    if isinstance(data, list):
        return data
    # Dict of lists (columnar format)
    if isinstance(data, dict):
        keys = list(data.keys())
        length = len(data[keys[0]]) if keys else 0
        return [{k: data[k][i] for k in keys} for i in range(length)]
    return []


def line(
    data: Any,
    x: str,
    y: str | list[str],
    title: str | None = None,
    color: str | list[str] | None = None,
    smooth: bool = False,
    area: bool = False,
    stacked: bool = False,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Line chart.

    Example:
        line(sales_data, x="date", y="revenue", title="Revenue Trend")

        # Multiple series
        line(data, x="date", y=["revenue", "costs"], title="Revenue vs Costs")
    """
    normalized_data = _normalize_data(data)
    y_fields = [y] if isinstance(y, str) else y

    return _add_to_current_container(Component(
        type="LineChart",
        props={
            "data": normalized_data,
            "xField": x,
            "yFields": y_fields,
            "title": title,
            "color": color,
            "smooth": smooth,
            "area": area,
            "stacked": stacked,
            "height": height,
            **props
        }
    ))


def bar(
    data: Any,
    x: str,
    y: str | list[str],
    title: str | None = None,
    color: str | list[str] | None = None,
    horizontal: bool = False,
    stacked: bool = False,
    grouped: bool = True,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Bar chart.

    Example:
        bar(category_data, x="category", y="sales", title="Sales by Category")

        # Horizontal bars
        bar(data, x="name", y="value", horizontal=True)
    """
    normalized_data = _normalize_data(data)
    y_fields = [y] if isinstance(y, str) else y

    return _add_to_current_container(Component(
        type="BarChart",
        props={
            "data": normalized_data,
            "xField": x,
            "yFields": y_fields,
            "title": title,
            "color": color,
            "horizontal": horizontal,
            "stacked": stacked,
            "grouped": grouped,
            "height": height,
            **props
        }
    ))


def pie(
    data: Any,
    values: str,
    names: str,
    title: str | None = None,
    donut: bool = False,
    show_labels: bool = True,
    show_legend: bool = True,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Pie/donut chart.

    Example:
        pie(category_data, values="amount", names="category", title="By Category")

        # Donut chart
        pie(data, values="count", names="status", donut=True)
    """
    normalized_data = _normalize_data(data)

    return _add_to_current_container(Component(
        type="PieChart",
        props={
            "data": normalized_data,
            "valueField": values,
            "nameField": names,
            "title": title,
            "donut": donut,
            "showLabels": show_labels,
            "showLegend": show_legend,
            "height": height,
            **props
        }
    ))


def scatter(
    data: Any,
    x: str,
    y: str,
    size: str | None = None,
    color: str | None = None,
    title: str | None = None,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Scatter plot.

    Example:
        scatter(data, x="height", y="weight", color="gender")

        # With size encoding
        scatter(data, x="x", y="y", size="value", title="Bubble Chart")
    """
    normalized_data = _normalize_data(data)

    return _add_to_current_container(Component(
        type="ScatterChart",
        props={
            "data": normalized_data,
            "xField": x,
            "yField": y,
            "sizeField": size,
            "colorField": color,
            "title": title,
            "height": height,
            **props
        }
    ))


def area(
    data: Any,
    x: str,
    y: str | list[str],
    title: str | None = None,
    color: str | list[str] | None = None,
    stacked: bool = True,
    gradient: bool = True,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Area chart.

    Example:
        area(data, x="date", y="value", title="Trend Over Time")

        # Stacked area
        area(data, x="date", y=["a", "b", "c"], stacked=True)
    """
    normalized_data = _normalize_data(data)
    y_fields = [y] if isinstance(y, str) else y

    return _add_to_current_container(Component(
        type="AreaChart",
        props={
            "data": normalized_data,
            "xField": x,
            "yFields": y_fields,
            "title": title,
            "color": color,
            "stacked": stacked,
            "gradient": gradient,
            "height": height,
            **props
        }
    ))


def gauge(
    value: float,
    max_value: float = 100,
    title: str | None = None,
    color: str | None = None,
    show_value: bool = True,
    format: str = "{value}%",
    size: int = 200,
    **props: Any,
) -> Component:
    """
    Gauge/radial chart.

    Example:
        gauge(75, title="Completion", format="{value}%")
    """
    return _add_to_current_container(Component(
        type="GaugeChart",
        props={
            "value": value,
            "maxValue": max_value,
            "title": title,
            "color": color,
            "showValue": show_value,
            "format": format,
            "size": size,
            **props
        }
    ))


def heatmap(
    data: Any,
    x: str,
    y: str,
    value: str,
    title: str | None = None,
    color_scale: list[str] | None = None,
    show_values: bool = True,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Heatmap chart.

    Example:
        heatmap(data, x="day", y="hour", value="count", title="Activity")
    """
    normalized_data = _normalize_data(data)

    return _add_to_current_container(Component(
        type="HeatmapChart",
        props={
            "data": normalized_data,
            "xField": x,
            "yField": y,
            "valueField": value,
            "title": title,
            "colorScale": color_scale,
            "showValues": show_values,
            "height": height,
            **props
        }
    ))


def funnel(
    data: Any,
    values: str,
    names: str,
    title: str | None = None,
    show_labels: bool = True,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Funnel chart.

    Example:
        funnel(conversion_data, values="count", names="stage", title="Conversion Funnel")
    """
    normalized_data = _normalize_data(data)

    return _add_to_current_container(Component(
        type="FunnelChart",
        props={
            "data": normalized_data,
            "valueField": values,
            "nameField": names,
            "title": title,
            "showLabels": show_labels,
            "height": height,
            **props
        }
    ))


def radar(
    data: Any,
    categories: str,
    values: str | list[str],
    title: str | None = None,
    fill: bool = True,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Radar/spider chart.

    Example:
        radar(skills_data, categories="skill", values="level")
    """
    normalized_data = _normalize_data(data)
    value_fields = [values] if isinstance(values, str) else values

    return _add_to_current_container(Component(
        type="RadarChart",
        props={
            "data": normalized_data,
            "categoryField": categories,
            "valueFields": value_fields,
            "title": title,
            "fill": fill,
            "height": height,
            **props
        }
    ))


def treemap(
    data: Any,
    values: str,
    names: str,
    parent: str | None = None,
    title: str | None = None,
    height: int = 300,
    **props: Any,
) -> Component:
    """
    Treemap chart.

    Example:
        treemap(file_data, values="size", names="name", parent="folder")
    """
    normalized_data = _normalize_data(data)

    return _add_to_current_container(Component(
        type="TreemapChart",
        props={
            "data": normalized_data,
            "valueField": values,
            "nameField": names,
            "parentField": parent,
            "title": title,
            "height": height,
            **props
        }
    ))


# Convenience alias
donut = lambda *args, **kwargs: pie(*args, donut=True, **kwargs)


__all__ = [
    "line",
    "bar",
    "pie",
    "donut",
    "scatter",
    "area",
    "gauge",
    "heatmap",
    "funnel",
    "radar",
    "treemap",
]
