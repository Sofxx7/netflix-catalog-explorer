# Building an Interactive Netflix Catalog Explorer with Streamlit

This is an individual article template. Each team member should rewrite it in
their own voice and include their own contribution before publishing it.

## Introduction

Interactive dashboards make it easier to move from a large table to a visual
question. In this project, our team created Netflix Catalog Explorer, an
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

The repository includes a GitHub Actions workflow. On every push to main or
pull request, it installs the dependencies, compiles the application, and
validates the dataset structure. The cloud application is configured to track
the repository so that new changes can be redeployed from the main branch.

Repository: [insert public repository URL]

Live application: [insert public application URL]

Video: [insert public video URL]

## Individual contribution

For this individual article, I contributed by [describe your contribution:
data preparation, interface design, chart selection, testing, documentation,
deployment, or video production]. This contribution helped the team connect
the visual analysis with a reproducible and publicly accessible application.

## Conclusion

This project shows that a concise visual report can combine exploratory
analysis with a reproducible software workflow. The final result is useful for
comparing catalog patterns while keeping the limitations of the source data
visible.
