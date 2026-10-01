"""Render a resume written in the tailor-resume Markdown format to .docx.

Usage:
    uv run --with python-docx render_docx.py resume.md [output.docx]

Format (one element per line):
    # Name
    contact line (first plain line after the name)
    ## Section heading
    ### Company, Location | Dates      (dates are right-aligned)
    *Job title*
    - bullet (supports **bold** spans)
    plain paragraph (supports **bold** spans)

Links become clickable: [text](url), email addresses (mailto:), and bare
web addresses with a path such as linkedin.com/in/name or github.com/user.
"""

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

FONT = "Calibri"
BODY_PT = 10.5
NAME_PT = 18
HEADING_PT = 11
RIGHT_TAB = Inches(7.5)


# [text](url), an email address, or a bare web address with a path
# (e.g. github.com/user). Bare domains without a path are left as text.
LINK_RE = re.compile(
    r"\[(?P<label>[^\]]+)\]\((?P<url>[^)]+)\)"
    r"|(?P<email>[\w.+-]+@[\w-]+(?:\.[\w-]+)+)"
    r"|(?P<web>(?:https?://)?(?:[\w-]+\.)+[a-z]{2,}/[^\s|,;)]+)"
)


def add_text_run(paragraph, text, size, bold, italic):
    run = paragraph.add_run(text)
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def add_hyperlink(paragraph, label, url, size, bold, italic):
    """Append a clickable hyperlink run (blue, underlined) to the paragraph."""
    r_id = paragraph.part.relate_to(url, RT.HYPERLINK, is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    props = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs"):
        fonts.set(qn(attr), FONT)
    props.append(fonts)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    props.append(color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    props.append(underline)
    if bold:
        props.append(OxmlElement("w:b"))
    if italic:
        props.append(OxmlElement("w:i"))
    half_points = OxmlElement("w:sz")
    half_points.set(qn("w:val"), str(int(size * 2)))
    props.append(half_points)
    run.append(props)
    text = OxmlElement("w:t")
    text.text = label
    text.set(qn("xml:space"), "preserve")
    run.append(text)
    link.append(run)
    paragraph._p.append(link)


def add_runs(paragraph, text, size=BODY_PT, bold=False, italic=False):
    """Add text to a paragraph, honoring **bold** spans and links."""
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if not part:
            continue
        part_bold = bold or i % 2 == 1
        pos = 0
        for match in LINK_RE.finditer(part):
            if match.start() > pos:
                add_text_run(paragraph, part[pos:match.start()], size, part_bold, italic)
            if match.group("label"):
                label, url = match.group("label"), match.group("url")
            elif match.group("email"):
                label = match.group("email")
                url = "mailto:" + label
            else:
                label = match.group("web")
                url = label if label.startswith("http") else "https://" + label
            add_hyperlink(paragraph, label, url, size, part_bold, italic)
            pos = match.end()
        if pos < len(part):
            add_text_run(paragraph, part[pos:], size, part_bold, italic)


def spacing(paragraph, before=0, after=2):
    fmt = paragraph.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)


def bottom_border(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for key, val in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "808080")):
        bottom.set(qn(f"w:{key}"), val)
    borders.append(bottom)
    p_pr.append(borders)


def render(md_path, out_path):
    doc = Document()
    section = doc.sections[0]
    section.left_margin = section.right_margin = Inches(0.5)
    section.top_margin = section.bottom_margin = Inches(0.625)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(BODY_PT)

    after_name = False
    for raw in Path(md_path).read_text().splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            p = doc.add_paragraph()
            add_runs(p, line[2:], size=NAME_PT, bold=True)
            spacing(p, after=0)
            after_name = True
        elif after_name:
            p = doc.add_paragraph()
            add_runs(p, line)
            spacing(p, after=4)
            after_name = False
        elif line.startswith("## "):
            p = doc.add_paragraph()
            add_runs(p, line[3:].upper(), size=HEADING_PT, bold=True)
            spacing(p, before=8, after=3)
            bottom_border(p)
        elif line.startswith("### "):
            left, _, dates = line[4:].partition(" | ")
            p = doc.add_paragraph()
            p.paragraph_format.tab_stops.add_tab_stop(RIGHT_TAB, WD_TAB_ALIGNMENT.RIGHT)
            add_runs(p, left, bold=True)
            if dates:
                add_runs(p, "\t" + dates, bold=True)
            spacing(p, before=6, after=0)
        elif line.startswith("*") and line.endswith("*") and not line.startswith("**"):
            p = doc.add_paragraph()
            add_runs(p, line.strip("*"), italic=True)
            spacing(p, after=2)
        elif line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_runs(p, line[2:])
            spacing(p, after=1)
        else:
            p = doc.add_paragraph()
            add_runs(p, line)
            spacing(p, after=2)

    doc.save(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".docx")
    render(src, dest)
    print(dest)
