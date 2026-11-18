"""Execute a team notebook headless with settings overrides, WITHOUT modifying the notebook file.

    .venv/bin/python -I results/skillguard_runs/main1000/run_notebook.py <notebook.ipynb> <executed_copy.ipynb> KEY=PYTHON_LITERAL ...

The settings cell (the first code cell that assigns every KEY) is copied in memory; each
`KEY = ...` line is replaced by `KEY = <literal>  # overridden by run_notebook.py`. The
executed copy (with all outputs) is saved to <executed_copy.ipynb> as provenance, next to
the run it produced. The original notebook on disk is never written.
"""

import ast
import hashlib
import re
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main():
    src, dst, *pairs = sys.argv[1:]
    overrides = {}
    for pair in pairs:
        key, _, literal = pair.partition("=")
        ast.literal_eval(literal)  # only plain Python literals are accepted
        overrides[key] = literal
    original = Path(src).read_bytes()
    nb = nbformat.reads(original.decode("utf-8"), as_version=4)
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        if all(re.search(rf"^{re.escape(k)}\s*=", cell.source, re.M) for k in overrides):
            for key, literal in overrides.items():
                # Replace the whole (possibly multi-line) top-level assignment statement.
                tree = ast.parse(cell.source)
                node = next(n for n in tree.body if isinstance(n, ast.Assign)
                            and any(isinstance(t, ast.Name) and t.id == key for t in n.targets))
                lines = cell.source.split("\n")
                lines[node.lineno - 1:node.end_lineno] = [f"{key} = {literal}  # overridden by run_notebook.py"]
                cell.source = "\n".join(lines)
            break
    else:
        raise SystemExit(f"no single code cell assigns all of {sorted(overrides)}")
    nb.metadata["run_notebook"] = {"source_notebook": src, "source_sha256": hashlib.sha256(original).hexdigest(),
                                   "overrides": overrides}
    client = NotebookClient(nb, timeout=None, kernel_name="python3",
                            resources={"metadata": {"path": str(Path(src).resolve().parent)}})
    try:
        client.execute()
    finally:
        Path(dst).parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(nb, dst)
    assert Path(src).read_bytes() == original, "source notebook changed during execution"
    print("executed", src, "->", dst)


if __name__ == "__main__":
    main()
