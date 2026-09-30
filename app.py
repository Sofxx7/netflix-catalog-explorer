from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "netflix_titles.csv"
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


st.set_page_config(
    page_title="Netflix Catalog Explorer",
    page_icon="🎬",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and prepare the public Netflix titles dataset."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    data = pd.read_csv(DATA_PATH)
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {sorted(missing_columns)}")

    data["date_added"] = pd.to_datetime(data["date_added"], errors="coerce")
    data["country"] = data["country"].fillna("Unknown").replace("", "Unknown")
    data["listed_in"] = data["listed_in"].fillna("Unknown").replace("", "Unknown")
    data["rating"] = data["rating"].fillna("Not rated")
    data["duration"] = data["duration"].fillna("Unknown")
    data["country_list"] = data["country"].str.split(", ")
    data["genre_list"] = data["listed_in"].str.split(", ")
    return data


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    """Apply the interactive sidebar filters."""
    st.sidebar.header("Filters")

    selected_type = st.sidebar.selectbox(
        "Content type",
        ["All"] + sorted(data["type"].dropna().unique().tolist()),
    )

    country_options = sorted(data["country_list"].explode().dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Country or territory",
        country_options,
        help="Leave empty to include all countries.",
    )

    genre_options = sorted(data["genre_list"].explode().dropna().unique().tolist())
    selected_genres = st.sidebar.multiselect(
        "Genre",
        genre_options,
        help="Leave empty to include all genres.",
    )

    year_min = int(data["release_year"].min())
    year_max = int(data["release_year"].max())
    selected_years = st.sidebar.slider(
        "Release year",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
    )

    filtered = data.copy()
    if selected_type != "All":
        filtered = filtered[filtered["type"] == selected_type]
    if selected_countries:
        filtered = filtered[
            filtered["country_list"].apply(
                lambda countries: any(country in selected_countries for country in countries)
            )
        ]
    if selected_genres:
        filtered = filtered[
            filtered["genre_list"].apply(
                lambda genres: any(genre in selected_genres for genre in genres)
            )
        ]
    return filtered[filtered["release_year"].between(selected_years[0], selected_years[1])]


def metric_columns(data: pd.DataFrame) -> None:
    """Render the summary indicators."""
    country_count = data["country_list"].explode().nunique()
    movie_count = int((data["type"] == "Movie").sum())
    show_count = int((data["type"] == "TV Show").sum())

    first, second, third, fourth = st.columns(4)
    first.metric("Titles", f"{len(data):,}")
    second.metric("Movies", f"{movie_count:,}")
    third.metric("TV shows", f"{show_count:,}")
    fourth.metric("Countries / territories", f"{country_count:,}")


def render_charts(data: pd.DataFrame) -> None:
    """Render the main visual report."""
    left, right = st.columns(2)

    with left:
        releases_by_year = (
            data.groupby(["release_year", "type"], as_index=False)
            .size()
            .rename(columns={"size": "titles"})
        )
        chart = px.line(
            releases_by_year,
            x="release_year",
            y="titles",
            color="type",
            markers=True,
            title="Titles by release year",
            labels={
                "release_year": "Release year",
                "titles": "Number of titles",
                "type": "Type",
            },
        )
        chart.update_layout(legend_title_text="")
        st.plotly_chart(chart, width="stretch")

    with right:
        type_counts = data["type"].value_counts().rename_axis("type").reset_index(name="titles")
        chart = px.pie(
            type_counts,
            names="type",
            values="titles",
            hole=0.55,
            title="Catalog composition",
            color="type",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#221F1F"},
        )
        chart.update_layout(legend_title_text="")
        st.plotly_chart(chart, width="stretch")

    left, right = st.columns(2)

    with left:
        country_counts = (
            data.explode("country_list")["country_list"]
            .value_counts()
            .head(10)
            .sort_values()
            .rename_axis("country")
            .reset_index(name="titles")
        )
        chart = px.bar(
            country_counts,
            x="titles",
            y="country",
            orientation="h",
            title="Top countries and territories",
            labels={"titles": "Titles", "country": ""},
            color="titles",
            color_continuous_scale=["#F8BBD0", "#E50914"],
        )
        chart.update_layout(coloraxis_showscale=False)
        st.plotly_chart(chart, width="stretch")

    with right:
        genre_counts = (
            data.explode("genre_list")["genre_list"]
            .value_counts()
            .head(10)
            .sort_values()
            .rename_axis("genre")
            .reset_index(name="titles")
        )
        chart = px.bar(
            genre_counts,
            x="titles",
            y="genre",
            orientation="h",
            title="Most frequent genres",
            labels={"titles": "Titles", "genre": ""},
            color="titles",
            color_continuous_scale=["#D7CCC8", "#5D4037"],
        )
        chart.update_layout(coloraxis_showscale=False)
        st.plotly_chart(chart, width="stretch")


def render_table(data: pd.DataFrame) -> None:
    """Render a compact result table."""
    st.subheader("Filtered catalog")
    table = data[
        ["title", "type", "release_year", "country", "rating", "duration", "listed_in"]
    ].sort_values(["release_year", "title"], ascending=[False, True])
    table = table.rename(
        columns={
            "title": "Title",
            "type": "Type",
            "release_year": "Release year",
            "country": "Country / territory",
            "rating": "Rating",
            "duration": "Duration",
            "listed_in": "Genres",
        }
    )
    st.markdown(
        table.head(100).to_html(index=False, classes="catalog-table", escape=True),
        unsafe_allow_html=True,
    )
    if len(table) > 100:
        st.caption("Showing the first 100 records from the current filter.")


try:
    catalog = load_data()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    [data-testid="stMetric"] {
        background: #fff7f7;
        border: 1px solid #f4d5d5;
        border-radius: 0.75rem;
        padding: 0.75rem;
    }
    .catalog-table {
        border-collapse: collapse;
        width: 100%;
        font-size: 0.88rem;
    }
    .catalog-table th, .catalog-table td {
        border-bottom: 1px solid #eeeeee;
        padding: 0.45rem;
        text-align: left;
        vertical-align: top;
    }
    .catalog-table th {
        background: #fff7f7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Netflix Catalog Explorer")
st.caption(
    "An interactive visual report for exploring the distribution of movies and TV shows "
    "by type, release year, country, and genre."
)

filtered_catalog = apply_filters(catalog)

if filtered_catalog.empty:
    st.warning("No titles match the selected filters. Try widening your selection.")
    st.stop()

metric_columns(filtered_catalog)
st.divider()
render_charts(filtered_catalog)
render_table(filtered_catalog)

st.caption(
    "Dataset source: Netflix Titles Dataset, available through the public repository linked "
    "in the project README. The dataset describes a catalog snapshot and should not be "
    "interpreted as the current Netflix catalog."
)
