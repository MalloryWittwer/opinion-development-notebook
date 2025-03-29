from pathlib import Path
import argparse
import markdown
from jinja2 import Template
from weasyprint import HTML, CSS


def main(out_dir: str, topic: str, author: str, image_url: str, **kwargs):
    out_dir = Path(out_dir)
    if not out_dir.exists():
        print(f"Directory {out_dir.resolve()} does not exist.")
        return
    
    with open("template.md", "r", encoding="utf-8") as f:
        md_template = Template(f.read())

    md_content = md_template.render(
        topic=topic,
        author=author,
        image_url=image_url,
    )

    html_body = markdown.markdown(md_content)

    with open("template.html", "r", encoding="utf-8") as f:
        html_template = Template(f.read())

    full_html = html_template.render(content=html_body)

    topic_slug = topic.lower().replace(" ", "-") + "_"
    out_file = out_dir / f"{topic_slug}notebook.pdf"
    HTML(string=full_html).write_pdf(target=out_file, stylesheets=[CSS('style.css')])

    print(f"Saved {out_file.resolve()}")


if __name__=='__main__':
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
        default="https://github.com/MalloryWittwer/opinion-development-notebook/blob/main/assets/self_reflection.png",
        help="Cover image URL.",
    )

    args = parser.parse_args()

    main(args.out_dir, args.topic, args.author, args.image_url)
