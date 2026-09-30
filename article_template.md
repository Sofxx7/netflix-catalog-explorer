# Building an Interactive Netflix Catalog Explorer with Streamlit

This is an individual article template. Rewrite it in your own voice before
publishing it.

## Introduction

Interactive dashboards make it easier to move from a large table to a visual
question. In this project, I created Netflix Catalog Explorer, an
interactive Streamlit application that explores a catalog snapshot of movies
and TV shows.

The objective was to combine data preparation, visual analysis, version
control, automated validation, and cloud publication in one small application.

## Tools and dataset

The application uses Python, pandas, Plotly, and Streamlit. The dataset is a
public netflix_titles.csv file containing title metadata such as content type,
release year, country, rating, duration, and genre.

Source:
https://github.com/japnitahuja/netflix-data-analysis/blob/main/netflix_titles.csv

The source represents a historical catalog snapshot. Therefore, the dashboard
is presented as an exploratory report about the dataset, not as a real-time
description of the current Netflix catalog.

## Dashboard construction

The application cleans missing values, separates multi-value country and genre
fields, and exposes filters for content type, country, genre, and release year.
The visual report contains summary indicators, a line chart of titles by
release year and type, a donut chart comparing movies and TV shows, horizontal
bar charts for countries and genres, and a table with the filtered records.

## Automation and publication

The repository includes GitHub Actions workflows. The quality workflow
compiles the application and validates the dataset. The publication workflow
regenerates the Plotly report and deploys it to GitHub Pages on every push to
main.

Repository: [insert public repository URL]

Live report: [insert public GitHub Pages URL]

Video: [insert public video URL]

## Individual contribution

I contributed by [describe your contribution: data preparation, interface
design, chart selection, testing, documentation, deployment, or video
production]. This work connected the visual analysis with a reproducible and
publicly accessible application.

## Conclusion

This project shows that a concise visual report can combine exploratory
analysis with a reproducible software workflow. The final result is useful for
comparing catalog patterns while keeping the limitations of the source data
visible.
