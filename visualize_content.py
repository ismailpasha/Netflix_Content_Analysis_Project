import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def extract_main_country(country_value: str) -> str:
    if pd.isna(country_value):
        return "Unknown"
    return str(country_value).split(",")[0].strip()


def extract_movie_minutes(duration_value: str) -> float:
    if pd.isna(duration_value) or "min" not in str(duration_value):
        return float("nan")
    return float(str(duration_value).split()[0])


def extract_tv_seasons(duration_value: str) -> float:
    if pd.isna(duration_value) or "Season" not in str(duration_value):
        return float("nan")
    return float(str(duration_value).split()[0])


def plot_content_type_counts(df: pd.DataFrame) -> None:
    type_counts = df["type"].value_counts().sort_values(ascending=False)

    plt.figure(figsize=(7, 5))
    sns.barplot(x=type_counts.index, y=type_counts.values, hue=type_counts.index, palette="Set2", legend=False)
    plt.title("Movies vs TV Shows Count")
    plt.xlabel("Content Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()


def plot_top_genres(df: pd.DataFrame) -> None:
    genres = df["listed_in"].dropna().str.split(",").explode().str.strip()
    top_genres = genres.value_counts().head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_genres.values, y=top_genres.index, hue=top_genres.index, palette="viridis", legend=False)
    plt.title("Top 10 Genres")
    plt.xlabel("Count")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.show()


def plot_titles_added_by_year(df: pd.DataFrame) -> None:
    date_series = pd.to_datetime(df["date_added"], errors="coerce")
    year_counts = date_series.dt.year.value_counts().sort_index()

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o")
    plt.title("Year-wise Trend of Content Added")
    plt.xlabel("Year")
    plt.ylabel("Number of Titles Added")
    plt.xticks(year_counts.index.astype(int), rotation=45)
    plt.tight_layout()
    plt.show()


def plot_top_countries_by_type(df: pd.DataFrame) -> None:
    country_df = df.copy()
    country_df["main_country"] = country_df["country"].apply(extract_main_country)

    top_countries = country_df["main_country"].value_counts().head(10).index
    filtered = country_df[country_df["main_country"].isin(top_countries)]

    plt.figure(figsize=(11, 6))
    sns.countplot(data=filtered, y="main_country", hue="type", order=top_countries)
    plt.title("Top 10 Countries by Content Type")
    plt.xlabel("Count")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()


def plot_rating_distribution_by_type(df: pd.DataFrame) -> None:
    rating_counts = (
        df.dropna(subset=["rating"])
        .groupby(["rating", "type"])
        .size()
        .reset_index(name="count")
    )

    top_ratings = (
        rating_counts.groupby("rating")["count"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )
    filtered = rating_counts[rating_counts["rating"].isin(top_ratings)]

    plt.figure(figsize=(11, 6))
    sns.barplot(data=filtered, x="rating", y="count", hue="type", order=top_ratings)
    plt.title("Top Ratings Split by Content Type")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_release_trend_by_type(df: pd.DataFrame) -> None:
    release_counts = (
        df.groupby(["release_year", "type"])
        .size()
        .reset_index(name="count")
    )
    recent_release_counts = release_counts[release_counts["release_year"] >= 2000]

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=recent_release_counts, x="release_year", y="count", hue="type", marker="o")
    plt.title("Release Trend by Content Type Since 2000")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Titles")
    plt.tight_layout()
    plt.show()


def plot_movie_duration_distribution(df: pd.DataFrame) -> None:
    movie_df = df[df["type"] == "Movie"].copy()
    movie_df["duration_minutes"] = movie_df["duration"].apply(extract_movie_minutes)
    movie_df = movie_df.dropna(subset=["duration_minutes"])

    plt.figure(figsize=(10, 5))
    sns.histplot(movie_df["duration_minutes"], bins=30, kde=True, color="teal")
    plt.title("Movie Duration Distribution")
    plt.xlabel("Duration (Minutes)")
    plt.ylabel("Number of Movies")
    plt.tight_layout()
    plt.show()


def plot_tv_seasons_distribution(df: pd.DataFrame) -> None:
    tv_df = df[df["type"] == "TV Show"].copy()
    tv_df["season_count"] = tv_df["duration"].apply(extract_tv_seasons)
    tv_df = tv_df.dropna(subset=["season_count"])

    season_order = sorted(tv_df["season_count"].unique())

    plt.figure(figsize=(10, 5))
    sns.countplot(data=tv_df, x="season_count", order=season_order, color="coral")
    plt.title("TV Show Seasons Distribution")
    plt.xlabel("Number of Seasons")
    plt.ylabel("Number of TV Shows")
    plt.tight_layout()
    plt.show()


def plot_top_genres_by_type(df: pd.DataFrame) -> None:
    genre_type_df = df[["type", "listed_in"]].dropna().copy()
    genre_type_df["listed_in"] = genre_type_df["listed_in"].str.split(",")
    genre_type_df = genre_type_df.explode("listed_in")
    genre_type_df["listed_in"] = genre_type_df["listed_in"].str.strip()

    top_genres = genre_type_df["listed_in"].value_counts().head(8).index
    filtered = genre_type_df[genre_type_df["listed_in"].isin(top_genres)]

    plt.figure(figsize=(11, 6))
    sns.countplot(data=filtered, y="listed_in", hue="type", order=top_genres)
    plt.title("Top Genres by Content Type")
    plt.xlabel("Count")
    plt.ylabel("Genre")
    plt.tight_layout()
    plt.show()


def create_visualizations(csv_path: Path) -> None:
    df = pd.read_csv(csv_path)

    sns.set_theme(style="whitegrid", palette="deep")

    plot_content_type_counts(df)
    plot_top_genres(df)
    plot_titles_added_by_year(df)
    plot_top_countries_by_type(df)
    plot_rating_distribution_by_type(df)
    plot_release_trend_by_type(df)
    plot_movie_duration_distribution(df)
    plot_tv_seasons_distribution(df)
    plot_top_genres_by_type(df)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Display Netflix content visualizations.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("netflix_titles.csv/netflix_titles.csv"),
        help="Path to the Netflix titles CSV file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_visualizations(args.csv)


if __name__ == "__main__":
    main()
