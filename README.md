# StravaAgent2

StravaAgent2 is a minimal command-line assistant that lets OpenAI’s
Responses API pick from a handful of pre-built tools (date lookup,
recent activities placeholder, and a National Weather Service forecast
for NYC) and then streams the model’s final answer back to the terminal.
It is intentionally small so you can experiment with tool-calling end to
end.

## Features

- Prompt loop that asks the user which capability they want and forwards
  the request to the OpenAI Responses API.
- Tool registry (`Tools/tools.py`) that exposes three callable
  functions: `get_date`, `get_activities`, and `get_nyc_weather`.
- Weather helpers (`Tools/Weather/`) that call the public
  [api.weather.gov](https://api.weather.gov) endpoints via `httpx` and
  format multi-period forecasts.
- Simple debugging helper (`Tools/Weather/testweather.py`) for printing
  “today’s” forecast without launching the agent.

## Requirements

- Python 3.13 (see `.python-version`).
- An OpenAI API key with access to the `o4-mini` model (set
  `OPENAI_API_KEY` in your environment).
- Dependencies from `pyproject.toml` (`openai`, `httpx`). The repo uses
  [uv](https://github.com/astral-sh/uv) for locking, but `pip` works as
  well.

## Installation

1. Create a virtual environment (example using `uv`):

   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

   or with pip:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r <(uv pip compile pyproject.toml)
   ```

2. Export your OpenAI key:

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

## Running the CLI

```bash
python main.py
```

1. The app asks “Please input your prompt”.
2. Type one of the tool names (e.g. `get_nyc_weather`) or `q` to quit.
3. The assistant calls `OpenAI().responses.create(...)` with the tool
   schema defined in `Tools/tools.py`.
4. When the model returns a `function_call`, `run_tools()` executes the
   matching Python implementation and feeds the result back into a second
   model call so you get a natural-language response.

## Weather Helpers

- `Tools/Weather/weather.py` wraps the National Weather Service API for
  both forecasts and alerts. It uses `httpx.AsyncClient` and is safe to
  call from any async context.
- `Tools/Weather/nyc_weather.py` provides `get_nyc_weather()` —
  a synchronous convenience wrapper that `run_tools()` calls so the CLI
  does not have to manage event loops.
- To inspect the raw forecast data without the agent, run:

  ```bash
  python -m Tools.Weather.testweather
  ```

## Repository Layout

- `main.py` – CLI entry point.
- `Tools/` – shared utilities and tool registry.
- `Tools/Weather/` – reusable NWS/weather helpers plus NYC-specific
  wrappers.
- `Root/` – duplicate copy of the same files kept for IDE experiments.
- `pyproject.toml` / `uv.lock` – packaging metadata and locked deps.

## Next Steps

- Flesh out `get_activities()` with real Strava API calls.
- Add tests (e.g. pytest) around the weather formatting helpers.
- Dry up the duplicate `Root/` copy once IDE experiments are done.
