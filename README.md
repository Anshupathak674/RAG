# Page-cited PDF RAG: a hands-on learning project

Repository: [Anshupathak674/RAG](https://github.com/Anshupathak674/RAG).

We are building a Python Retrieval-Augmented Generation (RAG) system incrementally, with Jupyter notebooks as the main learning interface. The eventual system will answer questions from PDFs and connect document-based claims to traceable source passages and physical PDF page numbers.

**Phase 1 is complete and validated; we are at its approval checkpoint.** Phase 2 requires explicit user approval. Completing a notebook or answering a conceptual question does not authorize the next phase.

## What Phase 1 includes

- An isolated Python environment and a project-specific Jupyter kernel.
- An executable introduction in [notebooks/01_rag_fundamentals.ipynb](notebooks/01_rag_fundamentals.ipynb).
- Environment checks and manually authored examples of provenance and page numbering.
- A fictional three-page document plan with known questions and expected supporting pages for later experiments.

PDF creation and parsing, chunking, embeddings, indexing, automatic retrieval, and LLM generation are deferred to later phases. No API account, key, paid service, or model download is needed for Phase 1.

## The system we are learning to build

An LLM's learned parameters do not provide a searchable copy of the user's documents or a reliable mapping from claims to PDF pages. RAG supplies selected external evidence when answering a question. It can improve access to relevant knowledge, but successful retrieval alone does not establish answer correctness.

```text
Document preparation (future phases)
PDF ingestion → page-aware text extraction → chunking
              → embedding generation → indexing

Question answering (future phases)
Question → retrieval → context augmentation → answer generation
                                        → citation attribution and validation
```

This is our intended dense-retrieval architecture; RAG can also use lexical or other retrieval methods. Embeddings and a vector database are architectural choices, not requirements for every RAG system.

Provenance must survive each transformation. We will retain document identifiers, original filenames, source locations, page relationships, and eventually chunk identifiers and text. A library's zero-based page index `0` corresponds to physical PDF page `1`; a printed label such as `i` or `12` may differ from both. Initial citations will use one-based physical PDF pages. A future chunk spanning pages must retain every relevant page relationship.

We will assess retrieval relevance, answer quality, and citation attribution separately. A valid source/page reference establishes a location; checking whether that location supports a claim is an additional task.

## Project files

```text
RAG/
├── README.md                          # Setup, decisions, and learning progress
├── .gitignore                         # Local environments and runtime artifacts
├── .python-version                    # Records Python 3.14.6; does not install it
├── requirements.in                    # Direct dependency constraints
├── requirements.txt                   # Exact installed-package snapshot
├── notebooks/
│   └── 01_rag_fundamentals.ipynb       # Phase 1 lesson and executable examples
├── scripts/
│   └── verify_phase1.py               # Notebook and environment verification
├── data/sample/
│   └── fixture_plan.json              # Fictional content and expected QA/pages
└── .venv/                             # Local Python environment and kernel
```

Jupyter and IPython state lives in ignored `.jupyter/` and `.ipython/` directories when using the launch commands below. We will add `src/` when reusable application logic exists and `tests/` when application behavior needs dedicated tests. No empty future pipeline modules are required now.

`fixture_plan.json` describes a planned three-page PDF and manually authored expectations. Its planned pages are **not extracted evidence**. Phase 2 will create the PDF and compare actual page-level extraction with those expectations.

## Environment and dependency choices

The initial environment is macOS on Apple Silicon with Python **3.14.6**. We use Python's built-in [`venv`](https://docs.python.org/3.14/library/venv.html) and `pip`: they provide isolation without introducing another environment manager at this stage. Conda, uv, or a project manager can become useful if Python-version management, native dependencies, or a more sophisticated lock workflow becomes necessary.

| Dependency | Direct constraint | Why it is present |
| --- | --- | --- |
| JupyterLab | `>=4.4,<5` | Browser-based notebook authoring and inspection |
| ipykernel | `>=6.29,<8` | Executes Python cells in the selected environment |
| nbclient | `>=0.10,<1` | Executes the notebook programmatically in a fresh kernel |
| nbformat | `>=5.10,<6` | Reads notebook files and validates their schema |

[JupyterLab](https://jupyter.org/install) is our local interface; a compatible editor's notebook UI is an alternative. Explicit kernel registration makes the interpreter choice visible in either interface. See the [IPython kernel installation guide](https://ipython.readthedocs.io/en/stable/install/kernel_install.html).

`requirements.in` records direct requirements and supported version ranges. `requirements.txt` is generated with [`pip freeze --all`](https://pip.pypa.io/en/stable/cli/pip_freeze/) and records the exact installed environment, including transitive dependencies and pip. It is an environment snapshot, **not a hash-verified, portable solver lock**. Matching Python, operating system, and architecture improves reproducibility; package availability and native compatibility can still differ elsewhere. Compatibility of Python 3.14 with future PDF and ML dependencies has not been validated; revisit the Python version when those phases begin.

## Set up or recreate the environment

Run these commands from the project root. First confirm that `python3` reports `3.14.6`; `.python-version` only records our choice and does not enforce it.

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m ipykernel install --prefix "$PWD/.venv" --name rag-learning --display-name "Python (RAG learning)"
```

The explicit `.venv/bin/python` paths avoid relying on shell activation. Register the kernel again after recreating or moving the environment, since its specification refers to the interpreter's location.

To intentionally update the Phase 1 environment from the direct constraints, review the resulting versions and revalidate before saving a new snapshot:

```bash
.venv/bin/python -m pip install --upgrade -r requirements.in
.venv/bin/python -m pip check
.venv/bin/python -m pip freeze --all > requirements.txt
```

Do not regenerate the snapshot merely to run the lesson. Dependency updates are changes to the project and should be reviewed.

## Open the notebook

```bash
IPYTHONDIR="$PWD/.ipython" \
JUPYTER_CONFIG_DIR="$PWD/.jupyter/config" \
JUPYTER_DATA_DIR="$PWD/.jupyter/data" \
JUPYTER_RUNTIME_DIR="$PWD/.jupyter/runtime" \
.venv/bin/jupyter lab notebooks/01_rag_fundamentals.ipynb
```

Select **Python (RAG learning)**, then restart the kernel and run all cells in order. A notebook file stores code, explanations, and outputs; the kernel is the Python process that executes its cells. Executing cells out of order can leave hidden state, so a clean run is part of validation.

## Verify Phase 1

```bash
IPYTHONDIR="$PWD/.ipython" \
JUPYTER_CONFIG_DIR="$PWD/.jupyter/config" \
JUPYTER_DATA_DIR="$PWD/.jupyter/data" \
JUPYTER_RUNTIME_DIR="$PWD/.jupyter/runtime" \
.venv/bin/python scripts/verify_phase1.py
```

The verifier validates notebook structure, executes it using [nbclient](https://nbclient.readthedocs.io/en/latest/client.html) in a fresh kernel, saves the executed notebook, and checks code execution counts and errors. It also verifies the environment, imports, pinned package versions, and project kernel. Schema validation alone cannot establish that code runs.

**Recorded validation on 20 October 2026:** Python 3.14.6; JupyterLab 4.6.4; ipykernel 7.4.0; nbformat 5.11.1; nbclient 0.11.0. All 10 code cells executed in order in a fresh `rag-learning` kernel, with zero error outputs, and the executed outputs were saved. Notebook schema, project files, kernel path, environment imports, and all 92 pinned package versions passed verification. `pip check` reported no broken requirements; the JupyterLab command reported version 4.6.4. The browser frontend was not visually inspected.

The notebook's hand-authored examples check simple metadata relationships and environment assumptions. They do not validate PDF extraction, automatic retrieval, semantic support for a generated claim, or LLM answer quality. An intentionally incorrect page-number assertion is caught in a clearly labeled demonstration; it is not an unexpected notebook error.

During setup, the restricted execution sandbox blocked package-index access and local kernel sockets; both required approved execution outside that sandbox. The initial execution also caught a syntax error in a teaching cell; it was corrected before the successful full run. Jupyter needs local process/socket access to run kernels. The verifier reports unexpected execution errors and does not overwrite the saved notebook on failure.

## Learning progress and decisions

| Item | Status or decision | Reason / revisit point |
| --- | --- | --- |
| Phase 1: setup and fundamentals | Complete; awaiting Phase 2 approval | Notebook executed and current environment validated |
| Phase 2: PDF ingestion and parsing | Pending explicit approval | Create the fixture, extract pages, preserve provenance, inspect limitations |
| Later phases | Planned, not implemented | Add chunking, representations, search, generation, and evaluation progressively |
| Local-first tooling | `venv`, pip, JupyterLab | Sufficient for the current requirements; revisit when dependency needs change |
| Application structure | Notebook plus a verification script | Add modules and dedicated application tests when there is reusable behavior |
| Citation convention | One-based physical PDF pages | Keep printed labels separate; retain page spans when chunking is introduced |
| Sample document | Fictional content plan with known QA/pages | Build controlled, inspectable expectations before evaluating extraction |
| Frameworks and external services | None in Phase 1 | Introduce an abstraction or service only when its benefit can be demonstrated |

Known limits: no PDF has been created or parsed in this phase; there is no retrieval or answer-generation implementation; manually selected examples do not demonstrate search quality; future library compatibility is unverified. Initial setup needs access to a package index, while the installed Phase 1 notebook needs no external service.

Next, subject to approval, Phase 2 will cover PDF ingestion, page-aware text extraction, source metadata, empty/scanned-page detection, and comparisons against our controlled fixture. It will not automatically authorize chunking or subsequent phases.
