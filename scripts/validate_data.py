from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).parents[1] / "data" / "netflix_titles.csv"
REQUIRED_COLUMNS = {
    "show_id",
    "type",
    "title",
    "country",
    "date_added",
    "release_year",
    "rating",
    "duration",
    "listed_in",
}


def main() -> None:
    if not DATA_PATH.exists():
        raise SystemExit(f"Dataset not found: {DATA_PATH}")

    data = pd.read_csv(DATA_PATH)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise SystemExit(f"Missing columns: {sorted(missing)}")
    if len(data) < 1000:
        raise SystemExit("The dataset is unexpectedly small.")

    print(f"Validated {len(data):,} rows and {len(data.columns)} columns.")


if __name__ == "__main__":
    main()
