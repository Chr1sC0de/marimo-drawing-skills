import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")

with app.setup:
    from pathlib import Path

    import marimo as mo

    from diagram_code import customer_api_diagram

    notebook_dir = Path(__file__).parent
    diagram_output_dir = notebook_dir / "rendered_diagrams"


@app.cell
def _():
    mo.md("## Example: AWS Architecture Diagram")


@app.cell
def _():
    customer_api_diagram_path = customer_api_diagram.build_diagram(
        diagram_output_dir / "customer_api_diagram"
    )

    return (customer_api_diagram_path,)


@app.cell
def _(customer_api_diagram_path):
    mo.image(customer_api_diagram_path, alt="AWS architecture diagram", width="100%")
    return


if __name__ == "__main__":
    app.run()
