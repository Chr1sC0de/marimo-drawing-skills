import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Starter notebook

        This marimo notebook is ready to edit.
        """
    )
    return


@app.cell
def _(mo):
    value = mo.ui.slider(start=1, stop=10, value=5, label="Value")
    value
    return (value,)


@app.cell
def _(mo, value):
    mo.md(f"Selected value: **{value.value}**")
    return


if __name__ == "__main__":
    app.run()
