# Netflix Catalog Explorer

Netflix Catalog Explorer is an interactive Streamlit visual report built with
Python, pandas, and Plotly. It explores a public catalog snapshot through
filters and charts for content type, release year, country or territory, and
genre.

## Main features

- Interactive filters for type, country, genre, and release year.
- Summary indicators for titles, movies, TV shows, and countries or territories.
- Charts for catalog composition, releases by year, top countries, and genres.
- A detailed table for the filtered catalog.

## Run locally

Create a Python virtual environment and install the packages listed in
requirements.txt. Then run the application with:

    streamlit run app.py

The application reads the versioned file at data/netflix_titles.csv.

## Automated quality check

Every push to main and every pull request runs the GitHub Actions workflow in
.github/workflows/quality.yml. The workflow installs the dependencies, compiles
the Python files, and validates the dataset schema and row count.

The public visual report is published through GitHub Pages by
.github/workflows/deploy-pages.yml. Every push to main regenerates the Plotly
report, uploads it as a Pages artifact, and deploys it automatically. This
creates a traceable path from the public repository to the cloud publication.

The Streamlit version remains available for local execution with streamlit run
app.py. The GitHub Pages version is the public report used for the delivery.

## Dataset

The project uses the public netflix_titles.csv catalog snapshot from
[japnitahuja/netflix-data-analysis](https://github.com/japnitahuja/netflix-data-analysis/blob/main/netflix_titles.csv).
The dataset is included in this repository so the application does not depend
on a live download at runtime. Its values represent a historical snapshot and
are not presented as the current Netflix catalog.

## Academic delivery checklist

- [ ] Public repository URL.
- [ ] Public GitHub Pages report URL.
- [ ] Evidence of the automated validation and redeployment path.
- [ ] Individual article URL.
- [ ] Public video URL, maximum five minutes.
- [ ] ZIP file containing the links and the required delivery notes.
