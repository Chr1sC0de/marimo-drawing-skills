import marimo

__generated_with = "0.23.4"
app = marimo.App(width="full")

with app.setup:
    from notebooks import slide_1, slide_2, slide_3

    async def render_slide(module):
        _results = await module.app.embed()
        return _results.output


@app.cell
async def _():
    await render_slide(slide_1)
    return


@app.cell
async def _():
    await render_slide(slide_2)
    return


@app.cell
async def _():
    await render_slide(slide_3)
    return


if __name__ == "__main__":
    app.run()
