# Marimo Drawing Skill

This context defines the language for a Codex skill that helps users create, render, and display drawings in marimo notebooks.

## Language

**Marimo drawing skill**:
A Codex skill that guides agents in creating and troubleshooting rendered drawing workflows in marimo notebooks.
_Avoid_: Diagrams skill, generic diagrams skill

**diagrams**:
The default Python backend for architecture diagrams as code.
_Avoid_: skills, Marimo drawing skill, pycairo

**pycairo**:
The Python binding for cairo used when custom drawing needs lower-level control than diagrams provides.
_Avoid_: diagrams replacement, default drawing tool

**drawing backend**:
A Python library used by a drawing module to produce a rendered artifact.
_Avoid_: drawing skill, notebook

**marimo auto-rendering**:
A marimo notebook pattern where a cell runs drawing code, writes an image artifact to a notebook-local output directory, and displays it with `mo.image`.
_Avoid_: automatic rendering, live rendering

**drawing module**:
An importable Python module that owns backend-specific drawing construction, rendering options, and output path creation.
_Avoid_: inline drawing cell

**diagram module**:
A drawing module that uses diagrams for architecture diagrams.
_Avoid_: inline diagram cell

**output stem**:
An extensionless path passed to diagram rendering so the output format determines the final file extension.
_Avoid_: image filename, PNG path

**rendered artifact**:
An image file produced from diagram code for display in a notebook or document.
_Avoid_: diagram source, checked-in output

**build_diagram function**:
A diagram module function that accepts an output stem, renders a diagram with `show=False`, and returns the rendered artifact path.
_Avoid_: render helper, notebook callback

**draw_surface function**:
A pycairo drawing module function that accepts an output stem, draws to a cairo surface, and returns the rendered artifact path.
_Avoid_: build_diagram, render helper

**direct import rendering**:
A marimo auto-rendering pattern where a notebook imports a diagram module and calls its build_diagram function directly.
_Avoid_: subprocess rendering, shell rendering

**CLI import path setup**:
A verification and execution convention where the agent prepends notebook module directories to `PYTHONPATH` before running marimo.
_Avoid_: notebook sys.path mutation

**marimo drawing reference**:
A Marimo drawing skill reference document that explains one drawing backend or rendering pattern.
_Avoid_: separate marimo skill

**custom drawing path**:
An alternative rendering path for manually drawing shapes, paths, fills, strokes, and surfaces.
_Avoid_: default diagram path

**pycairo marimo slide**:
An executable marimo example that renders a pycairo artifact and displays it with `mo.image`.
_Avoid_: documentation-only slide

**pycairo artifact**:
A PNG rendered artifact produced by drawing to a cairo image surface.
_Avoid_: SVG surface, PDF surface

**pycairo environment check**:
A verification script that imports cairo, reports pycairo/native cairo versions, and writes a tiny PNG artifact.
_Avoid_: install notes only

## Relationships

- The **Marimo drawing skill** teaches agents how to use **drawing backends** from marimo notebooks.
- **diagrams** is the default drawing tool for architecture diagrams.
- **pycairo** supports the **custom drawing path** when architecture diagrams need more manual control.
- **marimo auto-rendering** embeds **rendered artifacts** in a notebook workflow.
- A **drawing module** uses a **drawing backend** to create a **rendered artifact**.
- A **diagram module** is called by a marimo notebook during **marimo auto-rendering**.
- A **diagram module** accepts an **output stem** and returns the final image path.
- **marimo auto-rendering** creates **rendered artifacts** under a notebook-local output directory.
- A **diagram module** exposes a **build_diagram function** for marimo notebooks to call.
- A pycairo **drawing module** exposes a **draw_surface function** for marimo notebooks to call.
- **direct import rendering** is the default pattern for **marimo auto-rendering**.
- **CLI import path setup** keeps marimo notebooks focused on rendering rather than import bootstrapping.
- A **marimo drawing reference** extends the **Marimo drawing skill** rather than creating a separate skill.
- The **pycairo marimo slide** demonstrates the **custom drawing path** by running pycairo code.
- The **pycairo marimo slide** produces a **pycairo artifact** by default.
- A **pycairo environment check** verifies both the Python binding and the native cairo runtime.

## Example Dialogue

> **Dev:** "Is this a generic diagrams skill?"
> **Domain expert:** "No. It is a marimo drawing skill; diagrams is the default backend for architecture diagrams."

> **Dev:** "Should the Marimo drawing skill tell agents to import from `skills`?"
> **Domain expert:** "No. The Python architecture diagram backend is `diagrams`; `skills` refers to the Codex skill context."

> **Dev:** "Should I put all of the diagram code directly in the marimo cell?"
> **Domain expert:** "No. Put diagram construction in a diagram module and keep the marimo cell focused on rendering and display."

> **Dev:** "Why did rendering create `customer_api_diagram.png.png`?"
> **Domain expert:** "The render function expected an output stem, but it was given a filename with an extension."

> **Dev:** "Should I commit every file in `rendered_diagrams/`?"
> **Domain expert:** "No. Treat rendered artifacts as generated output unless an intentional example image is needed for documentation."

> **Dev:** "What should a marimo cell call to create the image?"
> **Domain expert:** "Call the diagram module's build_diagram function with an output stem, then pass the returned rendered artifact path to `mo.image`."

> **Dev:** "Should the notebook shell out to render the diagram?"
> **Domain expert:** "No. Use direct import rendering unless the diagram script specifically needs subprocess isolation."

> **Dev:** "Should a marimo notebook mutate `sys.path` so local modules import?"
> **Domain expert:** "No. The agent should prepend the notebook module directory to `PYTHONPATH` from the CLI before running or exporting."

> **Dev:** "Should marimo rendering be its own Codex skill?"
> **Domain expert:** "No. Keep diagrams and pycairo as references inside the Marimo drawing skill."

> **Dev:** "Should pycairo replace diagrams as the recommended drawing tool?"
> **Domain expert:** "No. Use diagrams by default; use pycairo as the custom drawing path when lower-level drawing control is needed."

> **Dev:** "Should a pycairo drawing module expose build_diagram?"
> **Domain expert:** "No. Use draw_surface so it is clear that pycairo draws to cairo surfaces rather than building diagrams nodes."

> **Dev:** "Can slide_3 just describe pycairo setup?"
> **Domain expert:** "No. It should be executable and render a pycairo artifact so the interface is proven."

> **Dev:** "Should the pycairo example default to SVG?"
> **Domain expert:** "No. Default to PNG so the output matches the existing marimo image display pattern."

> **Dev:** "Can we just document `pip install pycairo`?"
> **Domain expert:** "No. Add a pycairo environment check because pycairo depends on both the Python package and native cairo."

## Flagged Ambiguities

- "skills" was used to mean both the **Marimo drawing skill** and the **diagrams** Python library; resolved: use **Marimo drawing skill** for the Codex skill and **diagrams** for the Python package.
- "Diagrams skill" understated the scope; resolved: the skill assists with drawing in marimo notebooks, with **diagrams** as the default architecture diagram backend and **pycairo** as a custom drawing backend.
