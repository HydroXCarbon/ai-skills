"""Render a markdown research report to PDF.

Reads a markdown file produced by the fan-out-research skill's synthesizer
step and renders it as a PDF with the report's major headers preserved.

Tries renderers in order of fidelity:
  1. WeasyPrint (markdown -> HTML -> PDF, best for tables and styling)
  2. ReportLab (pure-Python, no system deps, basic layout)

If neither is available, prints install instructions and exits non-zero
so the skill can surface the failure to the user without claiming success.

Usage:
    python3 fan-out-research.py \\
        --markdown ./output/<slug>/report.md \\
        --output   ./output/<slug>/report.pdf \\
        --title    "<topic>" \\
        --date     2026-05-11
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def render_with_weasyprint(md_path: Path, pdf_path: Path, title: str, date: str) -> bool:
    try:
        import markdown as md_lib
        from weasyprint import CSS, HTML
    except ImportError:
        return False

    html_body = md_lib.markdown(
        md_path.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "toc"],
    )
    html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{title}</title></head>
<body>
<h1 class="report-title">{title}</h1>
<p class="report-date"><strong>Date:</strong> {date}</p>
<hr/>
{html_body}
</body></html>"""

    css = CSS(string="""
        @page { size: A4; margin: 2cm; }
        body { font-family: 'Helvetica', 'Arial', sans-serif; line-height: 1.5; color: #1a1a1a; }
        h1.report-title { font-size: 26pt; margin-bottom: 0.2em; }
        .report-date { color: #555; margin-top: 0; }
        h1, h2, h3 { color: #222; }
        h2 { border-bottom: 1px solid #ccc; padding-bottom: 0.2em; margin-top: 1.6em; }
        h3 { margin-top: 1.2em; }
        a { color: #0b5cad; word-break: break-all; }
        code { background: #f4f4f4; padding: 1px 4px; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 0.8em; border-radius: 4px; overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; margin: 1em 0; }
        th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: left; vertical-align: top; }
        th { background: #f0f0f0; }
        blockquote { border-left: 3px solid #ccc; margin-left: 0; padding-left: 1em; color: #555; }
    """)
    HTML(string=html_doc).write_pdf(target=str(pdf_path), stylesheets=[css])
    return True


def render_with_reportlab(md_path: Path, pdf_path: Path, title: str, date: str) -> bool:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            HRFlowable,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
        )
    except ImportError:
        return False

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=22, spaceAfter=6
    )
    date_style = ParagraphStyle(
        "DateStyle", parent=styles["Normal"], textColor="#555555", spaceAfter=12
    )
    h2_style = ParagraphStyle(
        "H2Style", parent=styles["Heading2"], spaceBefore=14, spaceAfter=6
    )
    h3_style = ParagraphStyle("H3Style", parent=styles["Heading3"])
    body_style = styles["BodyText"]

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=title,
    )

    story = [
        Paragraph(title, title_style),
        Paragraph(f"<b>Date:</b> {date}", date_style),
        HRFlowable(width="100%", thickness=0.5, color="#cccccc"),
        Spacer(1, 12),
    ]

    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line:
            story.append(Spacer(1, 6))
            continue
        if line.startswith("## "):
            story.append(Paragraph(line[3:], h2_style))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], h3_style))
        elif line.startswith("# "):
            story.append(Paragraph(line[2:], title_style))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args(argv)

    if not args.markdown.is_file():
        print(f"error: markdown not found: {args.markdown}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)

    if render_with_weasyprint(args.markdown, args.output, args.title, args.date):
        print(f"wrote {args.output} (weasyprint)")
        return 0

    if render_with_reportlab(args.markdown, args.output, args.title, args.date):
        print(f"wrote {args.output} (reportlab)")
        return 0

    print(
        "error: no PDF renderer available. Install one of:\n"
        "  pip install weasyprint markdown   # best fidelity (HTML+CSS, tables)\n"
        "  pip install reportlab             # pure-Python fallback",
        file=sys.stderr,
    )
    return 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))