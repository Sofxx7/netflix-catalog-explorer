import argparse
import textwrap
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


WIDTH = 1280
HEIGHT = 720
FPS = 24
BACKGROUND = (30, 20, 20)
PANEL = (51, 34, 34)
RED = (229, 9, 20)
LIGHT_RED = (255, 218, 218)
WHITE = (255, 255, 255)
MUTED = (221, 196, 196)
GOLD = (255, 184, 77)


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


FONT_TITLE = get_font(52, bold=True)
FONT_SUBTITLE = get_font(25)
FONT_SECTION = get_font(35, bold=True)
FONT_BODY = get_font(23)
FONT_SMALL = get_font(18)
FONT_METRIC = get_font(42, bold=True)


def make_base(section: str, title: str, subtitle: str = "") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 16), fill=RED)
    draw.text((64, 52), section.upper(), font=FONT_SMALL, fill=GOLD)
    draw.text((64, 92), title, font=FONT_TITLE, fill=WHITE)
    if subtitle:
        draw.text((66, 166), subtitle, font=FONT_SUBTITLE, fill=MUTED)
    return image, draw


def wrapped(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], width: int, font, fill) -> int:
    lines = textwrap.wrap(text, width=width)
    y = xy[1]
    for line in lines:
        draw.text((xy[0], y), line, font=font, fill=fill)
        y += font.size + 8
    return y


def metric(draw: ImageDraw.ImageDraw, x: int, label: str, value: str) -> None:
    draw.rounded_rectangle((x, 270, x + 250, 420), radius=18, fill=PANEL)
    draw.text((x + 24, 295), label, font=FONT_SMALL, fill=MUTED)
    draw.text((x + 24, 335), value, font=FONT_METRIC, fill=LIGHT_RED)


def create_slides(data: pd.DataFrame) -> list[tuple[Image.Image, int]]:
    data["country"] = data["country"].fillna("Unknown").replace("", "Unknown")
    data["listed_in"] = data["listed_in"].fillna("Unknown").replace("", "Unknown")
    data["genre_list"] = data["listed_in"].str.split(", ")

    movies = int((data["type"] == "Movie").sum())
    shows = int((data["type"] == "TV Show").sum())
    countries = int(
        data["country"].str.split(", ").explode().nunique()
    )
    genres = data.explode("genre_list")["genre_list"].value_counts().head(5)
    releases = data.groupby("release_year").size().sort_index()

    slides: list[tuple[Image.Image, int]] = []

    image, draw = make_base(
        "Visualization Reports or Dashboard",
        "Netflix Catalog Explorer",
        "An individual visual report built with Python, Streamlit, Plotly, and GitHub Actions.",
    )
    wrapped(
        draw,
        "A short demonstration of the data, visual report, automated deployment, and public result.",
        (66, 275),
        58,
        FONT_BODY,
        WHITE,
    )
    draw.text((66, 560), "https://sofxx7.github.io/netflix-catalog-explorer/", font=FONT_BODY, fill=LIGHT_RED)
    slides.append((image, 6))

    image, draw = make_base(
        "1. Data preparation",
        "A clear dataset makes a clear report",
        "The dashboard uses a historical snapshot of Netflix title metadata.",
    )
    metric(draw, 64, "Records", f"{len(data):,}")
    metric(draw, 340, "Movies", f"{movies:,}")
    metric(draw, 616, "TV shows", f"{shows:,}")
    metric(draw, 892, "Countries", f"{countries:,}")
    draw.text((66, 485), "Missing values are prepared and multi-value country and genre fields are separated.", font=FONT_BODY, fill=WHITE)
    draw.text((66, 555), "Source: public Netflix Titles Dataset", font=FONT_SMALL, fill=MUTED)
    slides.append((image, 8))

    image, draw = make_base(
        "2. Visual report",
        "Compare the catalog at a glance",
        "The report combines summary indicators with charts and a filtered table.",
    )
    draw.rounded_rectangle((66, 250, 500, 630), radius=20, fill=PANEL)
    center = (283, 435)
    radius = 120
    movie_angle = 360 * movies / (movies + shows)
    draw.pieslice(
        (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
        -90,
        -90 + movie_angle,
        fill=RED,
    )
    draw.pieslice(
        (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
        -90 + movie_angle,
        270,
        fill=GOLD,
    )
    draw.ellipse((center[0] - 55, center[1] - 55, center[0] + 55, center[1] + 55), fill=PANEL)
    draw.rectangle((135, 585, 160, 610), fill=RED)
    draw.text((175, 580), "Movies", font=FONT_SMALL, fill=WHITE)
    draw.rectangle((300, 585, 325, 610), fill=GOLD)
    draw.text((340, 580), "TV shows", font=FONT_SMALL, fill=WHITE)

    draw.rounded_rectangle((540, 250, 1216, 630), radius=20, fill=PANEL)
    draw.text((570, 280), "Most frequent genres", font=FONT_SECTION, fill=WHITE)
    max_count = int(genres.iloc[0])
    for index, (genre, count) in enumerate(genres.iloc[::-1].items()):
        y = 355 + index * 48
        draw.text((570, y), genre[:25], font=FONT_SMALL, fill=MUTED)
        draw.rounded_rectangle((800, y + 3, 1140, y + 28), radius=8, fill=(89, 58, 58))
        draw.rounded_rectangle((800, y + 3, 800 + int(340 * count / max_count), y + 28), radius=8, fill=RED)
        draw.text((1155, y), f"{count:,}", font=FONT_SMALL, fill=WHITE)
    slides.append((image, 8))

    image, draw = make_base(
        "3. Interaction",
        "Explore with filters",
        "The Streamlit version lets the user narrow the catalog without changing the source data.",
    )
    draw.rounded_rectangle((70, 260, 335, 620), radius=18, fill=PANEL)
    draw.text((100, 295), "Filters", font=FONT_SECTION, fill=WHITE)
    for index, label in enumerate(["Content type", "Country", "Genre", "Release year"]):
        y = 370 + index * 57
        draw.text((100, y), label, font=FONT_SMALL, fill=MUTED)
        draw.rounded_rectangle((100, y + 28, 300, y + 55), radius=6, fill=(84, 58, 58))
    chart_x, chart_y, chart_w, chart_h = 430, 285, 720, 280
    draw.rounded_rectangle((chart_x - 25, chart_y - 25, chart_x + chart_w + 25, chart_y + chart_h + 45), radius=18, fill=PANEL)
    draw.text((chart_x, chart_y - 5), "Titles by release year", font=FONT_SECTION, fill=WHITE)
    points = releases[releases.index >= 2000]
    values = points.to_numpy()
    if len(values):
        min_value = max(1, int(values.min()))
        max_value = int(values.max())
        coords = []
        for index, value in enumerate(values):
            x = chart_x + int(index * chart_w / max(1, len(values) - 1))
            y = chart_y + chart_h - 40 - int((value - min_value) / max(1, max_value - min_value) * 170)
            coords.append((x, y))
        if len(coords) > 1:
            draw.line(coords, fill=RED, width=5)
        for x, y in coords[:: max(1, len(coords) // 8)]:
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=LIGHT_RED)
    draw.text((chart_x, 590), "Filters update the indicators, charts, and table.", font=FONT_BODY, fill=LIGHT_RED)
    slides.append((image, 8))

    image, draw = make_base(
        "4. Automation",
        "From repository to public report",
        "Every push to main regenerates and publishes the visual report automatically.",
    )
    boxes = [
        (85, "GitHub\nrepository"),
        (435, "GitHub\nActions"),
        (785, "GitHub\nPages"),
    ]
    for index, (x, label) in enumerate(boxes):
        draw.rounded_rectangle((x, 330, x + 270, 500), radius=22, fill=PANEL)
        draw.text((x + 42, 375), label, font=FONT_SECTION, fill=WHITE, align="center")
        draw.text((x + 90, 525), "✓ verified", font=FONT_BODY, fill=LIGHT_RED)
        if index < len(boxes) - 1:
            draw.line((x + 280, 415, x + 335, 415), fill=GOLD, width=6)
            draw.polygon([(x + 335, 415), (x + 315, 400), (x + 315, 430)], fill=GOLD)
    slides.append((image, 8))

    image, draw = make_base(
        "5. Public result",
        "Ready to submit",
        "The source, report, automation, and delivery materials are prepared.",
    )
    links = [
        ("Repository", "github.com/Sofxx7/netflix-catalog-explorer"),
        ("Visual report", "sofxx7.github.io/netflix-catalog-explorer/"),
        ("Article", "Publish on Dev.to, Medium, or Hashnode"),
        ("Video", "Upload this demonstration to a public network"),
    ]
    for index, (label, value) in enumerate(links):
        y = 275 + index * 72
        draw.text((100, y), label, font=FONT_BODY, fill=GOLD)
        draw.text((330, y), value, font=FONT_BODY, fill=WHITE)
    draw.text((100, 600), "Thank you", font=FONT_SECTION, fill=LIGHT_RED)
    slides.append((image, 6))

    return slides


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="outputs/netflix_catalog_demo.mp4",
        help="Output MP4 path.",
    )
    args = parser.parse_args()

    root = Path(__file__).parents[1]
    data = pd.read_csv(root / "data" / "netflix_titles.csv")
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)

    writer = imageio_ffmpeg.write_frames(
        str(output),
        (WIDTH, HEIGHT),
        fps=FPS,
        codec="libx264",
        quality=7,
        pix_fmt_in="rgb24",
        pix_fmt_out="yuv420p",
    )
    writer.send(None)
    for slide, seconds in create_slides(data):
        frame = np.asarray(slide, dtype=np.uint8)
        for _ in range(FPS * seconds):
            writer.send(frame)
    writer.close()
    print(f"Created {output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
