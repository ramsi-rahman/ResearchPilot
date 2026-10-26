# ResearchPilot

ResearchPilot is a command-line tool that gathers web sources for a question and
saves a linked digest of excerpts. It is a lightweight research aid, not an
AI-powered answer engine.

## What it does

For each research question, ResearchPilot:

1. Searches the web using DuckDuckGo (no search API key required).
2. Fetches the pages returned by the search. If a page cannot be read, it uses
   that result's search snippet instead.
3. Takes an excerpt from each available source and includes its title and URL.
4. Checks basic consistency: whether findings have valid HTTP(S) URLs that match
   the sources collected.
5. Writes a Markdown report in `reports/` and saves the research run and source
   text in a local SQLite database at `storage/researchpilot.sqlite3`.

The verification step checks source links and report structure only. It does
**not** establish that a source is trustworthy, that a claim is true, or that
sources agree with each other. Review the linked sources before relying on the
report.

## What it does not do

- It does not use an LLM or any AI model. There is no default model, and
  `MODEL_API_KEY` is not used by the app.
- It does not independently summarize, compare, or fact-check sources. The
  report is a collection of source excerpts, not a generated conclusion.
- It does not require a DuckDuckGo API key. Search does require an internet
  connection and may be affected by the search service's availability or
  rate limits.

## Requirements

- Python 3.10 or newer
- Internet access

## Install

### Windows PowerShell

From the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Linux, macOS, or WSL

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Dependencies must be installed in the same Python environment used to run the
app.

## Run a research question

```bash
python main.py "What are the latest advances in grid-scale battery storage?"
```

To request a different number of search results (between 1 and 20):

```bash
python main.py --results 8 "What are the latest advances in grid-scale battery storage?"
```

The command prints the report path and saved run ID. Reports are Markdown files
in `reports/`. The local SQLite database stores the question, report path,
timestamp, and source details.

To list recent saved runs:

```bash
python main.py --history
```

## Configuration

No `.env` file or API keys are required for the current version. Optional
settings can be set in the environment or in a project-root `.env` file:

| Name | Default | Description |
| --- | --- | --- |
| `REPORT_DIRECTORY` | `reports/` | Directory for generated Markdown reports |
| `DATABASE_PATH` | `storage/researchpilot.sqlite3` | SQLite database location |
| `REQUEST_TIMEOUT` | `20` | HTTP timeout in seconds |
| `MAX_RESULTS` | `5` | Default number of search results, from 1 to 20 |
| `MAX_PAGE_CHARACTERS` | `12000` | Maximum extracted text per webpage |

`.env.example` shows the available optional settings. `.env` is ignored by Git;
do not commit secrets. LLM support may be added later, but model API settings do
not currently affect the application.

## Run tests

```bash
python -m pytest
```
