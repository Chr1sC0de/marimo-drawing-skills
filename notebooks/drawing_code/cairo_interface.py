from __future__ import annotations

import math
from pathlib import Path, PurePath


def draw_surface(
    output_stem: str | Path | PurePath,
    width: int = 960,
    height: int = 540,
    outformat: str = "png",
) -> Path:
    if outformat != "png":
        raise ValueError("Only PNG output is supported for this pycairo example.")
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive.")

    output_stem_path = Path(output_stem)
    if output_stem_path.suffix:
        raise ValueError(
            "output_stem must not include a file extension; set outformat instead."
        )

    try:
        import cairo
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "pycairo is required for this drawing example. "
            "Install it with `pip install pycairo` and ensure native cairo is available."
        ) from exc

    output_stem_path.parent.mkdir(parents=True, exist_ok=True)
    output_path = output_stem_path.with_suffix(f".{outformat}")

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    context.scale(width, height)

    _draw_interface(context)

    surface.write_to_png(str(output_path))
    surface.finish()
    return output_path


def _draw_interface(context) -> None:
    context.set_source_rgb(0.98, 0.99, 1.0)
    context.paint()

    _rounded_rectangle(context, 0.08, 0.12, 0.84, 0.76, 0.035)
    context.set_source_rgb(1.0, 1.0, 1.0)
    context.fill_preserve()
    context.set_source_rgb(0.18, 0.23, 0.31)
    context.set_line_width(0.006)
    context.stroke()

    context.select_font_face("Sans")
    context.set_source_rgb(0.09, 0.12, 0.18)
    context.set_font_size(0.06)
    context.move_to(0.14, 0.24)
    context.show_text("pycairo")

    context.set_font_size(0.032)
    context.move_to(0.14, 0.32)
    context.show_text("custom drawing surface")

    _draw_surface_stack(context)
    _draw_control_points(context)
    _draw_output_badge(context)


def _draw_surface_stack(context) -> None:
    colors = [
        (0.22, 0.41, 0.69),
        (0.15, 0.61, 0.47),
        (0.86, 0.53, 0.2),
    ]
    for index, color in enumerate(colors):
        x = 0.46 + index * 0.045
        y = 0.24 + index * 0.05
        _rounded_rectangle(context, x, y, 0.28, 0.2, 0.02)
        context.set_source_rgba(*color, 0.84)
        context.fill_preserve()
        context.set_source_rgb(0.11, 0.14, 0.2)
        context.set_line_width(0.004)
        context.stroke()


def _draw_control_points(context) -> None:
    context.set_source_rgb(0.11, 0.14, 0.2)
    context.set_line_width(0.008)
    context.move_to(0.17, 0.64)
    context.curve_to(0.33, 0.44, 0.5, 0.82, 0.72, 0.56)
    context.stroke()

    for x, y in [(0.17, 0.64), (0.33, 0.44), (0.5, 0.82), (0.72, 0.56)]:
        context.arc(x, y, 0.016, 0, 2 * math.pi)
        context.set_source_rgb(0.98, 0.99, 1.0)
        context.fill_preserve()
        context.set_source_rgb(0.22, 0.41, 0.69)
        context.set_line_width(0.006)
        context.stroke()


def _draw_output_badge(context) -> None:
    _rounded_rectangle(context, 0.66, 0.66, 0.18, 0.085, 0.018)
    context.set_source_rgb(0.09, 0.12, 0.18)
    context.fill()

    context.select_font_face("Sans")
    context.set_source_rgb(1.0, 1.0, 1.0)
    context.set_font_size(0.028)
    context.move_to(0.7, 0.715)
    context.show_text("PNG artifact")


def _rounded_rectangle(
    context,
    x: float,
    y: float,
    w: float,
    h: float,
    r: float,
) -> None:
    context.new_sub_path()
    context.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    context.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    context.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    context.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    context.close_path()
