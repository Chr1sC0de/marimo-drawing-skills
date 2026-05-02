# Diagrams Skill

This context defines the language for a Codex skill that helps users create, render, and display architecture diagrams from Python code.

## Language

**Diagrams skill**:
A Codex skill that guides agents in creating and troubleshooting architecture diagrams.
_Avoid_: skills package, diagrams library

**diagrams**:
The Python library used to define and render architecture diagrams as code.
_Avoid_: skills, Diagrams skill

**marimo auto-rendering**:
A marimo notebook pattern where a cell runs diagram code, writes an image artifact to a notebook-local output directory, and displays it with `mo.image`.
_Avoid_: automatic rendering, live rendering

**diagram module**:
An importable Python module that owns diagram construction, rendering options, and output path creation.
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

**direct import rendering**:
A marimo auto-rendering pattern where a notebook imports a diagram module and calls its build_diagram function directly.
_Avoid_: subprocess rendering, shell rendering

**marimo reference**:
The Diagrams skill reference document that explains direct import rendering for marimo notebooks.
_Avoid_: separate marimo skill

## Relationships

- The **Diagrams skill** teaches agents how to use **diagrams**.
- **marimo auto-rendering** embeds **diagrams** output in a notebook workflow.
- A **diagram module** is called by a marimo notebook during **marimo auto-rendering**.
- A **diagram module** accepts an **output stem** and returns the final image path.
- **marimo auto-rendering** creates **rendered artifacts** under a notebook-local output directory.
- A **diagram module** exposes a **build_diagram function** for marimo notebooks to call.
- **direct import rendering** is the default pattern for **marimo auto-rendering**.
- The **marimo reference** extends the **Diagrams skill** rather than creating a separate skill.

## Example Dialogue

> **Dev:** "Should the Diagrams skill tell agents to import from `skills`?"
> **Domain expert:** "No. The skill is named Diagrams, but the Python library is `diagrams`; `skills` refers to the Codex skill context."

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

> **Dev:** "Should marimo rendering be its own Codex skill?"
> **Domain expert:** "No. Add a marimo reference to the existing Diagrams skill because it is a usage pattern for diagrams."

## Flagged Ambiguities

- "skills" was used to mean both the **Diagrams skill** and the **diagrams** Python library; resolved: use **Diagrams skill** for the Codex skill and **diagrams** for the Python package.
