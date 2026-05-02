from __future__ import annotations

import math
from pathlib import Path, PurePath

Color = tuple[float, float, float]


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

    _draw_interface(cairo, context)

    surface.write_to_png(str(output_path))
    surface.finish()
    return output_path


def _draw_interface(cairo, context) -> None:
    _draw_background(cairo, context)
    _draw_header(context)
    _draw_pipeline(cairo, context)
    _draw_preview_card(cairo, context)
    _draw_contract_strip(context)


def _draw_background(cairo, context) -> None:
    gradient = cairo.LinearGradient(0, 0, 1, 1)
    gradient.add_color_stop_rgb(0, 0.96, 0.98, 1.0)
    gradient.add_color_stop_rgb(0.55, 0.99, 0.98, 0.94)
    gradient.add_color_stop_rgb(1, 0.95, 0.97, 0.99)
    context.set_source(gradient)
    context.paint()

    context.set_source_rgba(1.0, 1.0, 1.0, 0.34)
    for x in [0.08, 0.2, 0.32, 0.44, 0.56, 0.68, 0.8, 0.92]:
        context.move_to(x, 0)
        context.line_to(x, 1)
    for y in [0.12, 0.24, 0.36, 0.48, 0.6, 0.72, 0.84, 0.96]:
        context.move_to(0, y)
        context.line_to(1, y)
    context.set_line_width(0.0015)
    context.stroke()


def _draw_header(context) -> None:
    context.select_font_face("Sans", 0, 1)
    context.set_source_rgb(0.08, 0.12, 0.18)
    context.set_font_size(0.053)
    context.move_to(0.07, 0.14)
    context.show_text("pycairo custom rendering")

    context.select_font_face("Sans")
    context.set_font_size(0.024)
    context.set_source_rgb(0.38, 0.43, 0.5)
    context.move_to(0.071, 0.19)
    context.show_text("manual drawing control when diagrams is too structured")


def _draw_pipeline(cairo, context) -> None:
    cards = [
        (
            0.07,
            0.27,
            0.19,
            0.2,
            "marimo cell",
            "chooses an output stem",
            (0.19, 0.38, 0.72),
        ),
        (
            0.31,
            0.27,
            0.19,
            0.2,
            "draw_surface()",
            "owns cairo setup",
            (0.08, 0.58, 0.48),
        ),
        (
            0.55,
            0.27,
            0.19,
            0.2,
            "cairo surface",
            "paths, fills, strokes",
            (0.86, 0.5, 0.2),
        ),
        (
            0.76,
            0.27,
            0.17,
            0.2,
            "mo.image()",
            "displays PNG",
            (0.45, 0.28, 0.72),
        ),
    ]

    for index, card in enumerate(cards):
        _draw_interface_card(cairo, context, *card)
        if index < len(cards) - 1:
            _draw_arrow(
                context,
                card[0] + card[2] + 0.022,
                0.37,
                cards[index + 1][0] - 0.02,
                0.37,
            )


def _draw_interface_card(cairo, context, x, y, w, h, title, subtitle, color) -> None:
    _draw_shadow(context, x, y, w, h, 0.026)
    _rounded_rectangle(context, x, y, w, h, 0.025)
    context.set_source_rgb(1, 1, 1)
    context.fill()

    accent = cairo.LinearGradient(x, y, x + w, y)
    accent.add_color_stop_rgba(0, *color, 0.92)
    accent.add_color_stop_rgba(1, *color, 0.58)
    _rounded_rectangle(context, x, y, w, 0.035, 0.02)
    context.set_source(accent)
    context.fill()

    context.select_font_face("Sans", 0, 1)
    context.set_source_rgb(0.1, 0.14, 0.2)
    context.set_font_size(0.025)
    context.move_to(x + 0.024, y + 0.088)
    context.show_text(title)

    context.select_font_face("Sans")
    context.set_source_rgb(0.44, 0.48, 0.55)
    context.set_font_size(0.017)
    context.move_to(x + 0.024, y + 0.127)
    context.show_text(subtitle)

    _draw_card_icon(context, x + 0.024, y + 0.15, color)


def _draw_card_icon(context, x: float, y: float, color: Color) -> None:
    context.set_source_rgba(*color, 0.16)
    context.arc(x + 0.025, y, 0.024, 0, 2 * math.pi)
    context.fill()
    context.set_source_rgb(*color)
    context.set_line_width(0.004)
    context.move_to(x + 0.012, y)
    context.curve_to(x + 0.021, y - 0.018, x + 0.039, y + 0.018, x + 0.052, y)
    context.stroke()


def _draw_preview_card(cairo, context) -> None:
    _draw_shadow(context, 0.07, 0.55, 0.54, 0.31, 0.03)
    _rounded_rectangle(context, 0.07, 0.55, 0.54, 0.31, 0.03)
    context.set_source_rgb(1, 1, 1)
    context.fill()

    context.select_font_face("Sans", 0, 1)
    context.set_source_rgb(0.1, 0.14, 0.2)
    context.set_font_size(0.028)
    context.move_to(0.105, 0.62)
    context.show_text("custom path preview")

    context.select_font_face("Sans")
    context.set_font_size(0.018)
    context.set_source_rgb(0.47, 0.51, 0.58)
    context.move_to(0.105, 0.66)
    context.show_text("Bezier curves, control points, gradients, and overlays")

    path_gradient = cairo.LinearGradient(0.13, 0.77, 0.5, 0.64)
    path_gradient.add_color_stop_rgb(0, 0.16, 0.36, 0.78)
    path_gradient.add_color_stop_rgb(0.5, 0.08, 0.6, 0.48)
    path_gradient.add_color_stop_rgb(1, 0.86, 0.48, 0.18)
    context.set_source(path_gradient)
    context.set_line_width(0.014)
    context.move_to(0.13, 0.77)
    context.curve_to(0.24, 0.69, 0.36, 0.84, 0.53, 0.72)
    context.stroke()

    _draw_control_point(context, 0.13, 0.77, (0.16, 0.36, 0.78))
    _draw_control_point(context, 0.24, 0.69, (0.08, 0.6, 0.48))
    _draw_control_point(context, 0.36, 0.84, (0.86, 0.48, 0.18))
    _draw_control_point(context, 0.53, 0.72, (0.45, 0.28, 0.72))

    context.set_source_rgba(0.08, 0.12, 0.18, 0.18)
    context.set_line_width(0.0025)
    context.move_to(0.13, 0.77)
    context.line_to(0.24, 0.69)
    context.move_to(0.36, 0.84)
    context.line_to(0.53, 0.72)
    context.stroke()


def _draw_contract_strip(context) -> None:
    _draw_shadow(context, 0.66, 0.56, 0.27, 0.3, 0.03)
    _rounded_rectangle(context, 0.66, 0.56, 0.27, 0.3, 0.03)
    context.set_source_rgb(0.1, 0.14, 0.2)
    context.fill()

    context.select_font_face("Monospace", 0, 1)
    context.set_font_size(0.023)
    context.set_source_rgb(1, 1, 1)
    context.move_to(0.69, 0.635)
    context.show_text("draw_surface(")
    context.move_to(0.715, 0.685)
    context.show_text("output_stem")
    context.move_to(0.69, 0.735)
    context.show_text(") -> Path")

    _draw_pill(context, 0.69, 0.78, 0.17, 0.048, "PNG artifact")


def _draw_control_point(
    context,
    x: float,
    y: float,
    color: Color,
) -> None:
    context.arc(x, y, 0.017, 0, 2 * math.pi)
    context.set_source_rgb(1, 1, 1)
    context.fill_preserve()
    context.set_source_rgb(*color)
    context.set_line_width(0.006)
    context.stroke()


def _draw_pill(context, x: float, y: float, w: float, h: float, text: str) -> None:
    _rounded_rectangle(context, x, y, w, h, h / 2)
    context.set_source_rgb(0.86, 0.48, 0.18)
    context.fill()

    context.select_font_face("Sans", 0, 1)
    context.set_font_size(0.018)
    context.set_source_rgb(1, 1, 1)
    context.move_to(x + 0.025, y + 0.031)
    context.show_text(text)


def _draw_arrow(context, x1: float, y1: float, x2: float, y2: float) -> None:
    context.set_source_rgba(0.12, 0.16, 0.22, 0.55)
    context.set_line_width(0.004)
    context.move_to(x1, y1)
    context.line_to(x2, y2)
    context.stroke()

    context.move_to(x2, y2)
    context.line_to(x2 - 0.018, y2 - 0.012)
    context.line_to(x2 - 0.018, y2 + 0.012)
    context.close_path()
    context.fill()


def _draw_shadow(context, x: float, y: float, w: float, h: float, r: float) -> None:
    _rounded_rectangle(context, x + 0.008, y + 0.012, w, h, r)
    context.set_source_rgba(0.08, 0.12, 0.18, 0.13)
    context.fill()


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
