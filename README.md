# Static Site Generator

A Python-based static site generator that turns Markdown content into HTML pages using a reusable HTML template.

## What it does

- Reads Markdown files from the `content/` directory
- Converts them into HTML using a lightweight Markdown parser
- Injects the generated HTML into `template.html`
- Copies static assets from `static/` into the output folder
- Writes the final result to `docs/`

## Project structure

- `content/` – source Markdown content
- `static/` – CSS and other static assets copied to the output
- `template.html` – page layout used for generated pages
- `src/` – Python implementation and tests
- `docs/` – generated site output

## Live demo

The project is published on GitHub Pages:

https://ttg17.github.io/static-site-generator/

## How to run

From the project root:

```bash
python3 src/main.py
cd docs && python3 -m http.server 8888
```

This will generate the site in the `docs/` folder.

A convenience script is also included:

```bash
./main.sh
```

That script runs the generator and then serves the output locally on port 8888.

## Testing

```bash
./test.sh
```

This runs the project test suite with unittest.

## Notes

- Pages are generated recursively from the `content/` folder.
- The title is taken from the first `#` heading in each Markdown file.
- The generator supports a basic Markdown feature set, including headings, paragraphs, lists, blockquotes, and code blocks.
