import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

API_URL = "https://official-joke-api.appspot.com/random_joke"
DATA_DIR = Path("data")


def fetch_joke(api_url: str = API_URL, timeout: int = 10) -> dict:
    """Fetch one random joke from the API and return it as a dict."""
    with urlopen(api_url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def write_outputs(now: datetime, joke: dict, data_dir: Path = DATA_DIR) -> None:
    """Write JSON outputs + a plain text joke.txt (overwritten each run)."""
    data_dir.mkdir(exist_ok=True)

    payload = {"timestamp": now.isoformat(), "joke": joke}

    (data_dir / f"{now.date()}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (data_dir / "latest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    setup = joke.get("setup", "")
    punchline = joke.get("punchline", "")
    (data_dir / "joke.txt").write_text(f"{setup}\n{punchline}\n", encoding="utf-8")


def main() -> None:
    now = datetime.now(timezone.utc)
    joke = fetch_joke()
    write_outputs(now, joke)


if __name__ == "__main__":
    main()
