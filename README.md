# mywhoosh

A lightweight, modular, and dependency-free Python client for the unofficial [MyWhoosh API](https://github.com/mywhoosh-community/mywhoosh-api).

Easily authenticate and retrieve your scheduled workouts from MyWhoosh in your Python scripts and automations.

---

## Features

- **Zero External Dependencies:** Built entirely with Python's standard library (`urllib`, `dataclasses`, `json`, etc.).
- **Modular & Reusable:** Import `MyWhooshClient` directly into your scripts or tools.
- **Convenient Data Models:** Structured `WorkoutTask` dataclass providing clean field access (`date`, `name`, `description`, `tss`, and full raw payload).
- **Flexible Date Filtering:** Supports Unix timestamps, ISO date strings (`YYYY-MM-DD`), and quick upcoming window queries (`days=7`).
- **Environment & `.env` Support:** Automatic loading of `.env` files for seamless credential management.
- **CLI Ready:** Run directly with `python3 -m mywhoosh` or `python3 mywhoosh_test.py`.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/workouts-script.git
cd workouts-script
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

*(The `.env` file is already listed in `.gitignore` to prevent committing secrets).*

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

You can run the module directly from the command line:

```bash
python3 -m mywhoosh
```

### CLI Arguments

```bash
# Query a specific date range using ISO dates
python3 -m mywhoosh --start-date 2026-10-25 --end-date 2026-11-01

# Query using Unix timestamps
python3 -m mywhoosh --start-date 1792368000 --end-date 1792972799
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

## Contributing & References

- Unofficial API Documentation: [mywhoosh-community/mywhoosh-api](https://github.com/mywhoosh-community/mywhoosh-api)

---

## Disclaimer

This is an unofficial, community-driven project and is not affiliated with, endorsed, or supported by MyWhoosh.
