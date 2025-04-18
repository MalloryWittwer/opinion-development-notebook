from pathlib import Path
import argparse
from jinja2 import Template
from weasyprint import HTML, CSS
from io import BytesIO


def generate_pdf(
    topic: str,
    author: str,
    image_url: str,
    facts: str = None,
    trust: str = None,
    missing: str = None,
    interpretations: str = None,
    difficult: str = None,
    assumptions: str = None,
    emotions: str = None,
    experiences: str = None,
    yourself: str = None,
    others: str = None,
    positive: str = None,
    negative: str = None,
    summary: str = None,
    target: str = None,
    out_file: Path = None,
) -> BytesIO:
    with open("templates/notebook.html", "r", encoding="utf-8") as f:
        html_template = Template(f.read())

    full_html = html_template.render(
        topic=topic,
        author=author,
        image_url=image_url,
        facts=facts,
        trust=trust,
        missing=missing,
        interpretations=interpretations,
        difficult=difficult,
        assumptions=assumptions,
        emotions=emotions,
        experiences=experiences,
        yourself=yourself,
        others=others,
        positive=positive,
        negative=negative,
        summary=summary,
    )

    if target == "bytes":
        out_file = BytesIO()
        HTML(string=full_html).write_pdf(
            target=out_file, stylesheets=[CSS("static/notebook.css")]
        )
        out_file.seek(0)  # Reset the stream position to the beginning
    else:
        HTML(string=full_html).write_pdf(
            target=out_file, stylesheets=[CSS("static/notebook.css")]
        )

    return out_file


def main(out_dir: str, topic: str, author: str, image_url: str):
    out_dir = Path(out_dir)
    if not out_dir.exists():
        print(f"Directory {out_dir.resolve()} does not exist.")
        return

    topic_slug = topic.lower().replace(" ", "-")
    if topic_slug != "":
        topic_slug += "_"

    out_file = out_dir / f"{topic_slug}notebook.pdf"
    saved_file = generate_pdf(topic, author, image_url, out_file=out_file)

    print(f"Saved {saved_file.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Opinion Development Notebook CLI")

    parser.add_argument(
        "out_dir",
        help="Output directory.",
    )
    parser.add_argument(
        "-t",
        "--topic",
        default="",
        help="Booklet topic.",
    )
    parser.add_argument(
        "-a",
        "--author",
        default="",
        help="Booklet author.",
    )
    parser.add_argument(
        "-i",
        "--image-url",
        default="https://raw.githubusercontent.com/MalloryWittwer/opinion-development-notebook/refs/heads/main/assets/self_reflection.png",
        help="Cover image URL.",
    )

    args = parser.parse_args()

    main(args.out_dir, args.topic, args.author, args.image_url)
