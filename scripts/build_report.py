from pathlib import Path

import pandas as pd
import plotly.express as px
from plotly.io import to_html


ROOT = Path(__file__).parents[1]
DATA_PATH = ROOT / "data" / "netflix_titles.csv"
OUTPUT_PATH = ROOT / "site" / "index.html"


def prepare_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data["country"] = data["country"].fillna("Unknown").replace("", "Unknown")
    data["listed_in"] = data["listed_in"].fillna("Unknown").replace("", "Unknown")
    data["rating"] = data["rating"].fillna("Not rated")
    data["duration"] = data["duration"].fillna("Unknown")
    data["country_list"] = data["country"].str.split(", ")
    data["genre_list"] = data["listed_in"].str.split(", ")
    return data


def chart_html(figure, include_plotlyjs=False) -> str:
    figure.update_layout(
        template="plotly_white",
        margin={"l": 30, "r": 20, "t": 60, "b": 30},
        font={"family": "Inter, Arial, sans-serif"},
    )
    return to_html(
        figure,
        include_plotlyjs=include_plotlyjs,
        full_html=False,
        config={"displaylogo": False, "responsive": True},
    )


def build_page(data: pd.DataFrame) -> str:
    total = len(data)
    movies = int((data["type"] == "Movie").sum())
    shows = int((data["type"] == "TV Show").sum())
    countries = int(data["country_list"].explode().nunique())

    releases = (
        data.groupby(["release_year", "type"], as_index=False)
        .size()
        .rename(columns={"size": "titles"})
    )
    release_chart = px.line(
        releases,
        x="release_year",
        y="titles",
        color="type",
        markers=True,
        title="Titles by release year",
        labels={"release_year": "Release year", "titles": "Titles", "type": "Type"},
    )

    type_counts = data["type"].value_counts().rename_axis("type").reset_index(name="titles")
    type_chart = px.pie(
        type_counts,
        names="type",
        values="titles",
        hole=0.55,
        title="Catalog composition",
        color="type",
        color_discrete_map={"Movie": "#E50914", "TV Show": "#221F1F"},
    )

    country_counts = (
        data.explode("country_list")["country_list"]
        .value_counts()
        .head(10)
        .sort_values()
        .rename_axis("country")
        .reset_index(name="titles")
    )
    country_chart = px.bar(
        country_counts,
        x="titles",
        y="country",
        orientation="h",
        title="Top countries and territories",
        labels={"titles": "Titles", "country": ""},
        color="titles",
        color_continuous_scale=["#F8BBD0", "#E50914"],
    )
    country_chart.update_layout(coloraxis_showscale=False)

    genre_counts = (
        data.explode("genre_list")["genre_list"]
        .value_counts()
        .head(10)
        .sort_values()
        .rename_axis("genre")
        .reset_index(name="titles")
    )
    genre_chart = px.bar(
        genre_counts,
        x="titles",
        y="genre",
        orientation="h",
        title="Most frequent genres",
        labels={"titles": "Titles", "genre": ""},
        color="titles",
        color_continuous_scale=["#D7CCC8", "#5D4037"],
    )
    genre_chart.update_layout(coloraxis_showscale=False)

    recent_titles = data.sort_values(
        ["release_year", "title"], ascending=[False, True]
    ).head(20)
    rows = "\n".join(
        f"<tr><td>{row.title}</td><td>{row.type}</td><td>{int(row.release_year)}</td>"
        f"<td>{row.rating}</td><td>{row.duration}</td></tr>"
        for row in recent_titles.itertuples()
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Netflix Catalog Explorer</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{ margin: 0; background: #f8f5f5; color: #221f1f;
      font-family: Inter, Arial, sans-serif; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 2.5rem 1.25rem; }}
    .hero {{ background: linear-gradient(135deg, #221f1f, #721b1b);
      border-radius: 1.25rem; color: white; padding: 2rem; }}
    h1 {{ margin: 0 0 .5rem; font-size: clamp(2rem, 5vw, 3.5rem); }}
    .hero p {{ max-width: 760px; line-height: 1.6; color: #ffecec; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr);
      gap: 1rem; margin: 1.25rem 0; }}
    .metric, .panel {{ background: white; border: 1px solid #eadede;
      border-radius: 1rem; padding: 1rem; box-shadow: 0 8px 24px #32101012; }}
    .metric span {{ display: block; color: #765e5e; font-size: .85rem; }}
    .metric strong {{ display: block; color: #b20710; font-size: 1.8rem; margin-top: .3rem; }}
    .charts {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }}
    th, td {{ border-bottom: 1px solid #eee; padding: .65rem; text-align: left; }}
    th {{ background: #fff7f7; }}
    footer {{ color: #765e5e; font-size: .88rem; line-height: 1.5; margin-top: 1.5rem; }}
    a {{ color: #b20710; }}
    @media (max-width: 800px) {{
      .metrics, .charts {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>🎬 Netflix Catalog Explorer</h1>
      <p>An interactive Plotly visual report about a historical catalog snapshot
      of movies and TV shows. Use the chart controls to hover, zoom, and compare
      patterns across the dataset.</p>
    </section>
    <section class="metrics">
      <div class="metric"><span>Titles</span><strong>{total:,}</strong></div>
      <div class="metric"><span>Movies</span><strong>{movies:,}</strong></div>
      <div class="metric"><span>TV shows</span><strong>{shows:,}</strong></div>
      <div class="metric"><span>Countries / territories</span><strong>{countries:,}</strong></div>
    </section>
    <section class="charts">
      <div class="panel">{chart_html(release_chart, include_plotlyjs="cdn")}</div>
      <div class="panel">{chart_html(type_chart)}</div>
      <div class="panel">{chart_html(country_chart)}</div>
      <div class="panel">{chart_html(genre_chart)}</div>
    </section>
    <section class="panel" style="margin-top: 1rem">
      <h2>Recent release years in the dataset</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Title</th><th>Type</th><th>Release year</th>
          <th>Rating</th><th>Duration</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </section>
    <footer>
      Dataset source:
      <a href="https://github.com/japnitahuja/netflix-data-analysis/blob/main/netflix_titles.csv">
      public Netflix Titles Dataset</a>. This is a historical snapshot, not a
      real-time description of the current Netflix catalog. The report is
      generated with Python, pandas, and Plotly and published automatically
      through GitHub Actions and GitHub Pages.
    </footer>
  </main>
</body>
</html>
"""


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        build_page(prepare_data()),
        encoding="utf-8",
    )
    print(f"Built {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
