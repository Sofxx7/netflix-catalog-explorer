# Building an Interactive Netflix Catalog Explorer with Streamlit and Plotly

## Introduction

Data visualization helps transform a large table into questions that are
easier to explore. For this activity, I created Netflix Catalog Explorer, an
interactive visual report about a historical catalog snapshot of movies and TV
shows.

The project combines data preparation, interactive visualization, automated
validation, and public cloud publication in one small application.

## Tools and dataset

The application was developed with Python, pandas, Plotly, and Streamlit. The
dataset is a public netflix_titles.csv file containing metadata such as
content type, title, country, date added, release year, rating, duration, and
genre.

Dataset source:
https://github.com/japnitahuja/netflix-data-analysis/blob/main/netflix_titles.csv

The dataset contains 8,807 records: 6,131 movies and 2,676 TV shows. It
includes titles from 1925 to 2021 and 128 countries or territories after
splitting the multi-value country field. These values describe the dataset
snapshot and should not be interpreted as the current Netflix catalog.

## Dashboard construction

The application prepares missing values and separates the country and genre
fields so they can be explored as individual categories. The Streamlit version
provides filters for content type, country, genre, and release year.

The visual report includes:

1. Summary indicators for titles, movies, TV shows, and countries or
   territories.
2. A line chart showing titles by release year and content type.
3. A donut chart comparing movies and TV shows.
4. Horizontal bar charts for the most frequent countries and genres.
5. A table with recent titles from the dataset.

The public report is generated with Plotly and includes interactive hover,
zoom, and chart controls.

## Automation and publication

The source code is available in a public GitHub repository:

https://github.com/Sofxx7/netflix-catalog-explorer

The repository contains two GitHub Actions workflows. The quality workflow
compiles the Python files and validates the dataset schema. The publication
workflow generates the static Plotly report, uploads it as a Pages artifact,
and deploys it to GitHub Pages whenever changes are pushed to the main branch.

Public visual report:

https://sofxx7.github.io/netflix-catalog-explorer/

This workflow makes the publication reproducible: a new version of the report
can be generated and deployed from the repository without manually copying
files to the hosting service.

## Personal contribution

I prepared the dataset, developed the dashboard interface, selected the
visualizations, created the validation workflow, and configured the public
deployment. I also prepared the explanation and video demonstration required
for the activity.

## Conclusion

This project shows how a small Python application can connect exploratory data
analysis with interactive visualizations and a reproducible deployment
process. It also keeps the limitations of the dataset visible by presenting
the results as an analysis of a historical snapshot rather than a real-time
Netflix catalog.
