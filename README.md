# py-mywhoosh

A lightweight, modular, and dependency-free Python client for the unofficial [MyWhoosh API](https://github.com/mywhoosh-community/mywhoosh-api).

Easily authenticate and retrieve your scheduled workouts from MyWhoosh in your Python scripts, automations, and terminal.

---

## Features

- **Zero External Dependencies:** Built entirely with Python's standard library (`urllib`, `dataclasses`, `json`, etc.).
- **Modular & Reusable:** Import `MyWhooshClient` directly into your scripts or tools.
- **Convenient Data Models:** Structured `WorkoutTask` dataclass providing clean field access (`date`, `name`, `description`, `tss`, and full raw payload).
- **Flexible Date Filtering:** Supports Unix timestamps, ISO date strings (`YYYY-MM-DD`), and quick upcoming window queries (`days=7`).
- **Environment & `.env` Support:** Automatic loading of `.env` files for seamless credential management.
- **CLI & Entrypoint Ready:** Run with `mywhoosh`, `python3 -m mywhoosh`, or `python3 mywhoosh_test.py`.
- **Fully Typed:** Includes PEP 561 `py.typed` marker for IDEs and type checkers (e.g. Mypy).

---

## Installation

### From PyPI

```bash
pip install py-mywhoosh
```

### From GitHub Source

```bash
pip install git+https://github.com/diogorsousa/py-mywhoosh.git
```

### Local Development

```bash
git clone https://github.com/diogorsousa/py-mywhoosh.git
cd py-mywhoosh
pip install -e .
```

> **Requirement:** Python 3.10 or higher.

---

## Configuration

Set your MyWhoosh account credentials either via a `.env` file or standard environment variables.

### Option 1: `.env` File (Recommended)

Copy the provided example and add your password:

```bash
cp .env.example .env
```

Edit `.env`:
```env
MYWHOOSH_USERNAME=your-email@example.com
MYWHOOSH_PASSWORD=your-password
```

*(The `.env` file is listed in `.gitignore` to prevent committing secrets).*

### Option 2: Environment Variables

```bash
export MYWHOOSH_USERNAME="your-email@example.com"
export MYWHOOSH_PASSWORD="your-password"
```

---

## Quick Start

### 1. Python Library Usage

```python
from mywhoosh import MyWhooshClient

# Automatically load credentials from .env or environment
client = MyWhooshClient.from_env()

# Retrieve scheduled workouts for the upcoming 7 days
tasks = client.get_upcoming_tasks(days=7)

for task in tasks:
    print(f"[{task.date}] {task.name} - TSS: {task.tss}")
    print(f"Description: {task.description}\n")
```

### 2. Custom Date Range Queries

You can query any custom date window using Unix timestamps or ISO date strings (`YYYY-MM-DD`):

```python
from mywhoosh import MyWhooshClient

client = MyWhooshClient.from_env()

# Query using ISO date strings
tasks = client.get_tasks(start_date="2026-10-25", end_date="2026-11-05")

# Convert tasks to dictionary format
tasks_data = [task.to_dict() for task in tasks]
print(tasks_data)
```

### 3. Explicit Credentials or Existing Token

```python
from mywhoosh import MyWhooshClient

# Authenticate with credentials
client = MyWhooshClient(username="user@example.com", password="password")

# Or initialize with a pre-existing JWT access token
client = MyWhooshClient(token="eyJhbGciOiJIUzI1NiIs...")
```

---

## CLI Usage

When installed, you can run the command-line interface directly with `mywhoosh` or `python3 -m mywhoosh`:

```bash
# Query workouts for upcoming 7 days (loads .env if present)
mywhoosh
```

### CLI Arguments

```bash
# Query a specific date range using ISO dates
mywhoosh --start-date 2026-10-25 --end-date 2026-11-01

# Query using Unix timestamps
mywhoosh --start-date 1792368000 --end-date 1792972799
```

Output:
```json
[
  {
    "TaskStartedTimeEpoc": "2026-10-27",
    "TaskName": "Base Miles #3",
    "TaskDescription": "Continuing our focus on building base fitness...",
    "TSS": 34
  },
  {
    "TaskStartedTimeEpoc": "2026-10-29",
    "TaskName": "Escalating 3min VO2max",
    "TaskDescription": "There's no escaping the fact that VO2max intervals are hard work...",
    "TSS": 60
  }
]
```

---

## Running Tests

Run the test suite using standard library `unittest`:

```bash
python3 -m unittest discover tests
```

---

## Publishing to PyPI

### Option 1: Automated Release via GitHub Actions (Recommended)

This repository includes a GitHub Actions workflow configured for [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/):

1. On PyPI, add a **Trusted Publisher** for `py-mywhoosh`:
   - Owner: `diogorsousa`
   - Repository name: `py-mywhoosh`
   - Workflow name: `publish.yml`
2. Create and publish a GitHub Release with a tag (e.g., `v0.1.0`).
3. GitHub Actions will automatically build and publish the wheel and sdist to PyPI.

### Option 2: Manual Build & Upload

```bash
# Install packaging tools
pip install build twine

# Build distribution packages
python3 -m build

# Check distribution packages
twine check dist/*

# Upload to PyPI
twine upload dist/*
```

---

## API Reference

### `MyWhooshClient`

| Method | Description |
| :--- | :--- |
| `MyWhooshClient(username=None, password=None, token=None, timeout=30.0)` | Initializes the client. |
| `from_env(env_path=".env")` | Creates client instance reading credentials from `.env` or environment. |
| `authenticate() -> str` | Performs authentication with MyWhoosh and caches the JWT access token. |
| `get_upcoming_tasks(days=7) -> list[WorkoutTask]` | Fetches scheduled tasks from today through `days` ahead. |
| `get_tasks(start_date, end_date) -> list[WorkoutTask]` | Fetches tasks within the specified date range. |
| `get_raw_task_list(start_date, end_date) -> dict` | Fetches the raw unprocessed response from the MyWhoosh task service. |

### `WorkoutTask` Dataclass

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `date` | `str` | Formatted workout date (`YYYY-MM-DD`). |
| `name` | `str` | Name of the workout or task. |
| `description` | `str` | Detailed description of the workout session. |
| `tss` | `int \| float` | Training Stress Score. |
| `task_id` | `str` | Unique ID of the task. |
| `raw` | `dict` | Complete original dictionary returned by the API. |
| `to_dict()` | `dict` | Returns dictionary with essential fields (`TaskStartedTimeEpoc`, `TaskName`, `TaskDescription`, `TSS`). |

### Exceptions

- `MyWhooshError`: Base exception for the library.
- `AuthenticationError`: Raised on login failures or invalid credentials.
- `ApiError`: Raised when the MyWhoosh API returns an HTTP or payload error.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Disclaimer

This is an unofficial, community-driven project and is not affiliated with, endorsed, or supported by MyWhoosh.
