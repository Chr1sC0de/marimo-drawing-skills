import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")

with app.setup:
    from pathlib import Path

    import marimo as mo

    from drawing_code import cairo_interface

    notebook_dir = Path(__file__).parent
    drawing_output_dir = notebook_dir / "rendered_diagrams"


@app.cell
def _():
    mo.md(
        """
        ## Pycairo Custom Drawing Interface

        `diagrams` is the default tool for architecture diagrams. Use pycairo when a
        drawing needs custom paths, fills, strokes, transforms, or surface-level control.
        """
    )
    return


@app.cell
def _():
    cairo_artifact_path = cairo_interface.draw_surface(
        drawing_output_dir / "pycairo_interface"
    )
    return (cairo_artifact_path,)


@app.cell
def _(cairo_artifact_path):
    mo.image(cairo_artifact_path, alt="Pycairo custom drawing interface", width="100%")
    return


if __name__ == "__main__":
    app.run()
