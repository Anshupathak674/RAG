"""Validate and execute the Phase 1 notebook using the project's Python kernel.

Run from any directory with the project's .venv/bin/python. Successful execution
replaces the notebook's saved outputs. A failing run leaves the file unchanged
and exits with an exception; inspect the failing cell in the terminal.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from importlib.metadata import version


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENT = PROJECT_ROOT / ".venv"
NOTEBOOK = PROJECT_ROOT / "notebooks" / "01_rag_fundamentals.ipynb"
KERNEL_NAME = "rag-learning"


def main() -> None:
    """Check setup, run a fresh kernel, validate outputs, then save the notebook."""
    if Path(sys.prefix).resolve() != ENVIRONMENT.resolve():
        raise RuntimeError("Use this project's .venv/bin/python to run this script.")

    # Keep runtime files and IPython history inside this workspace.
    local_paths = {
        "IPYTHONDIR": PROJECT_ROOT / ".ipython",
        "JUPYTER_CONFIG_DIR": PROJECT_ROOT / ".jupyter" / "config",
        "JUPYTER_DATA_DIR": PROJECT_ROOT / ".jupyter" / "data",
        "JUPYTER_RUNTIME_DIR": PROJECT_ROOT / ".jupyter" / "runtime",
        "XDG_CACHE_HOME": PROJECT_ROOT / ".cache",
    }
    for name, path in local_paths.items():
        path.mkdir(parents=True, exist_ok=True)
        os.environ[name] = str(path)

    import nbformat
    from jupyter_client.kernelspec import KernelSpecManager
    from nbclient import NotebookClient

    # Check the saved environment snapshot without printing environment variables.
    pins = (PROJECT_ROOT / "requirements.txt").read_text(encoding="utf-8")
    package_count = 0
    for line in pins.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        package, expected = line.split("==", maxsplit=1)
        actual = version(package)
        if actual != expected:
            raise RuntimeError(f"Dependency drift: {package}: {actual} != {expected}")
        package_count += 1

    kernel = KernelSpecManager().get_kernel_spec(KERNEL_NAME)
    expected_executable = ENVIRONMENT / "bin" / "python"
    # Compare paths without resolving the venv symlink to its base interpreter.
    if Path(kernel.argv[0]).absolute() != expected_executable.absolute():
        raise RuntimeError("The rag-learning kernel points to a different Python.")

    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    if notebook.metadata.kernelspec.name != KERNEL_NAME:
        raise RuntimeError("Notebook metadata must select the rag-learning kernel.")
    client = NotebookClient(
        notebook,
        timeout=60,
        startup_timeout=60,
        kernel_name=KERNEL_NAME,
        allow_errors=False,
        resources={"metadata": {"path": str(NOTEBOOK.parent)}},
    )
    client.execute()

    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    counts = [cell.execution_count for cell in code_cells]
    if not code_cells or counts != list(range(1, len(code_cells) + 1)):
        raise RuntimeError(f"Unexpected execution order: {counts}")
    errors = [
        output
        for cell in code_cells
        for output in cell.outputs
        if output.output_type == "error"
    ]
    if errors:
        raise RuntimeError(f"Notebook has {len(errors)} error outputs.")
    nbformat.validate(notebook)
    nbformat.write(notebook, NOTEBOOK)
    print(json.dumps({
        "notebook": str(NOTEBOOK.relative_to(PROJECT_ROOT)),
        "schema": "valid",
        "kernel": KERNEL_NAME,
        "code_cells_executed": len(code_cells),
        "error_outputs": len(errors),
        "pinned_packages_checked": package_count,
        "outputs_saved": True,
    }, indent=2))


if __name__ == "__main__":
    main()
