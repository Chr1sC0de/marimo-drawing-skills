import marimo

__generated_with = "0.23.4"
app = marimo.App(width="full")

with app.setup:
    import marimo as mo


@app.cell
def _():
    mo.md("# Hello World")


if __name__ == "__main__":
    app.run()
