"""Build the integrated avocado research proposal PDF from Markdown sources."""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import urlparse

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    PageTemplate,
    PageBreak,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT = OUTPUT_DIR / "avocado-research-proposal.pdf"

SOURCES = [
    ROOT / "proposal" / "avocado-research-proposal.md",
    ROOT / "appendices" / "appendix-a-existing-papers.md",
    ROOT / "appendices" / "appendix-b-bibliography.md",
    ROOT / "appendices" / "appendix-c-public-datasets.md",
    ROOT / "appendices" / "appendix-d-hardware-catalogue.md",
    ROOT / "appendices" / "appendix-e-mathematical-models.md",
    ROOT / "appendices" / "appendix-f-software-stack.md",
    ROOT / "appendices" / "appendix-g-repository-structure.md",
    ROOT / "appendices" / "appendix-h-data-quality.md",
    ROOT / "appendices" / "appendix-i-ml-results.md",
    ROOT / "appendices" / "appendix-j-statistical-plan.md",
    ROOT / "appendices" / "appendix-k-reproducibility.md",
    ROOT / "appendices" / "appendix-l-risk-evidence.md",
]


def register_fonts() -> None:
    candidates = {
        "ProposalSans": Path("C:/Windows/Fonts/arial.ttf"),
        "ProposalSans-Bold": Path("C:/Windows/Fonts/arialbd.ttf"),
        "ProposalSans-Italic": Path("C:/Windows/Fonts/ariali.ttf"),
        "ProposalMono": Path("C:/Windows/Fonts/consola.ttf"),
    }
    fallback = {
        "ProposalSans": "Helvetica",
        "ProposalSans-Bold": "Helvetica-Bold",
        "ProposalSans-Italic": "Helvetica-Oblique",
        "ProposalMono": "Courier",
    }
    for name, path in candidates.items():
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))
        else:
            pdfmetrics.registerFont(
                TTFont(name, str(Path("C:/Windows/Fonts/arial.ttf")))
            )
    addMapping("ProposalSans", 0, 0, "ProposalSans")
    addMapping("ProposalSans", 1, 0, "ProposalSans-Bold")
    addMapping("ProposalSans", 0, 1, "ProposalSans-Italic")
    _ = fallback


def normalize(text: str) -> str:
    replacements = {
        "\u00a0": " ",
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u00ad": "",
        "\ufeff": "",
        "\u2080": "0",
        "\u2081": "1",
        "\u2082": "2",
        "\u2083": "3",
        "\u2084": "4",
        "\u2085": "5",
        "\u2086": "6",
        "\u2087": "7",
        "\u2088": "8",
        "\u2089": "9",
        "\u207a": "+",
        "\u207b": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def inline_markup(text: str) -> str:
    """Convert a safe subset of Markdown inline markup to ReportLab XML."""
    text = normalize(text)
    tokens: list[str] = []

    def protect(match: re.Match[str]) -> str:
        tokens.append(match.group(0))
        return f"@@TOKEN{len(tokens)-1}@@"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", protect, text)
    text = re.sub(r"`([^`]+)`", protect, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"__([^_]+)__", r"<b>\1</b>", text)

    for index, token in enumerate(tokens):
        if token.startswith("["):
            match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token)
            assert match
            label, target = match.groups()
            label = html.escape(normalize(label), quote=False)
            target = html.escape(normalize(target), quote=True)
            parsed = urlparse(target)
            if parsed.scheme in {"http", "https"}:
                replacement = (
                    f'<link href="{target}" color="#1261A0"><u>{label}</u></link>'
                )
            else:
                replacement = f'<font color="#486581">{label}</font>'
        else:
            content = html.escape(normalize(token[1:-1]), quote=False)
            replacement = (
                f'<font name="ProposalMono" color="#334E68">{content}</font>'
            )
        text = text.replace(f"@@TOKEN{index}@@", replacement)
    text = text.replace("\\(", "").replace("\\)", "")
    return text


def strip_markdown(text: str) -> str:
    text = normalize(text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`#]", "", text)
    return text.strip()


def build_styles():
    base = getSampleStyleSheet()
    body_font = "ProposalSans"
    bold_font = "ProposalSans-Bold"
    mono_font = "ProposalMono"
    styles = {}
    styles["Body"] = ParagraphStyle(
        "Body",
        parent=base["BodyText"],
        fontName=body_font,
        fontSize=9.2,
        leading=13.2,
        textColor=colors.HexColor("#243B53"),
        alignment=TA_LEFT,
        spaceAfter=5.5,
        allowWidows=0,
        allowOrphans=0,
    )
    styles["Small"] = ParagraphStyle(
        "Small",
        parent=styles["Body"],
        fontSize=7.4,
        leading=10,
        textColor=colors.HexColor("#486581"),
    )
    styles["Caption"] = ParagraphStyle(
        "Caption",
        parent=styles["Small"],
        fontName="ProposalSans-Italic",
        alignment=TA_CENTER,
        spaceBefore=3,
        spaceAfter=9,
    )
    styles["Bullet"] = ParagraphStyle(
        "Bullet",
        parent=styles["Body"],
        leftIndent=14,
        firstLineIndent=-8,
        bulletIndent=4,
        spaceAfter=3,
    )
    styles["Numbered"] = ParagraphStyle(
        "Numbered",
        parent=styles["Body"],
        leftIndent=18,
        firstLineIndent=-12,
        bulletIndent=0,
        spaceAfter=3,
    )
    heading_specs = {
        1: (19, 23, "#102A43", 16, 10),
        2: (15, 19, "#0B6E75", 13, 7),
        3: (12.2, 15.5, "#1F5A7A", 10, 5),
        4: (10.5, 13.5, "#334E68", 8, 3),
    }
    for level, (size, leading, color, before, after) in heading_specs.items():
        styles[f"Heading{level}"] = ParagraphStyle(
            f"Heading{level}",
            parent=base[f"Heading{min(level, 3)}"],
            fontName=bold_font,
            fontSize=size,
            leading=leading,
            textColor=colors.HexColor(color),
            spaceBefore=before,
            spaceAfter=after,
            keepWithNext=True,
        )
    styles["Code"] = ParagraphStyle(
        "Code",
        parent=base["Code"],
        fontName=mono_font,
        fontSize=6.8,
        leading=9.2,
        textColor=colors.HexColor("#243B53"),
        leftIndent=7,
        rightIndent=7,
        spaceBefore=4,
        spaceAfter=7,
    )
    styles["Math"] = ParagraphStyle(
        "Math",
        parent=styles["Code"],
        fontSize=7.4,
        leading=10,
        alignment=TA_CENTER,
    )
    styles["Callout"] = ParagraphStyle(
        "Callout",
        parent=styles["Body"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#102A43"),
        borderColor=colors.HexColor("#9FB3C8"),
        borderWidth=0.75,
        borderPadding=8,
        backColor=colors.HexColor("#F0F4F8"),
        spaceBefore=6,
        spaceAfter=8,
    )
    return styles


class ProposalDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="proposal-frame",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        self.addPageTemplates(
            [PageTemplate(id="proposal-pages", frames=[frame], onPage=page_header)]
        )

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            match = re.fullmatch(r"Heading([1-3])", style)
            if match:
                level = int(match.group(1)) - 1
                text = strip_markdown(flowable.getPlainText())
                key = f"toc-{self.page}-{abs(hash((text, self.page)))}"
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level, closed=False)
                self.notify("TOCEntry", (level, text, self.page, key))


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.setFont("ProposalSans", 7)
                self.setFillColor(colors.HexColor("#627D98"))
                self.drawRightString(
                    A4[0] - 18 * mm,
                    12 * mm,
                    f"Page {self._pageNumber} of {page_count}",
                )
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)


def page_header(canv, doc):
    if doc.page <= 1:
        return
    canv.saveState()
    canv.setStrokeColor(colors.HexColor("#BCCCDC"))
    canv.setLineWidth(0.4)
    canv.line(18 * mm, A4[1] - 15 * mm, A4[0] - 18 * mm, A4[1] - 15 * mm)
    canv.setFont("ProposalSans", 7)
    canv.setFillColor(colors.HexColor("#627D98"))
    canv.drawString(
        18 * mm,
        A4[1] - 11.5 * mm,
        "Multimodal Non-Destructive Avocado Ripeness Characterization",
    )
    canv.drawRightString(
        A4[0] - 18 * mm,
        A4[1] - 11.5 * mm,
        "Research proposal - 30 July 2026",
    )
    canv.restoreState()


def image_flowable(path: Path, max_width: float, max_height: float):
    from PIL import Image as PILImage

    with PILImage.open(path) as source:
        width, height = source.size
    scale = min(max_width / width, max_height / height)
    return Image(str(path), width=width * scale, height=height * scale)


def table_flowable(rows: list[list[str]], styles, available_width: float):
    columns = max(len(row) for row in rows)
    rows = [row + [""] * (columns - len(row)) for row in rows]
    if columns == 1:
        widths = [available_width]
    else:
        raw = []
        for column in range(columns):
            longest = max(
                min(len(strip_markdown(row[column])), 70) for row in rows
            )
            raw.append(max(9, longest))
        total = sum(raw)
        widths = [available_width * value / total for value in raw]
        min_width = 18 * mm
        widths = [max(min_width, value) for value in widths]
        if sum(widths) > available_width:
            factor = available_width / sum(widths)
            widths = [value * factor for value in widths]

    font_size = 6.5 if columns >= 5 else 7.2
    leading = 8.4 if columns >= 5 else 9.3
    cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Small"],
        fontSize=font_size,
        leading=leading,
        textColor=colors.HexColor("#243B53"),
    )
    header_style = ParagraphStyle(
        "TableHeader",
        parent=cell_style,
        fontName="ProposalSans-Bold",
        textColor=colors.white,
    )
    data = []
    for r_index, row in enumerate(rows):
        data.append(
            [
                Paragraph(inline_markup(cell), header_style if r_index == 0 else cell_style)
                for cell in row
            ]
        )
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F5A7A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BCCCDC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F5F7FA")],
                ),
            ]
        )
    )
    return table


def parse_markdown(path: Path, styles, available_width: float):
    lines = normalize(path.read_text(encoding="utf-8")).splitlines()
    story = []
    paragraph_lines: list[str] = []
    code_lines: list[str] = []
    math_lines: list[str] = []
    in_code = False
    in_math = False

    def flush_paragraph():
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(line.strip() for line in paragraph_lines)
            story.append(Paragraph(inline_markup(text), styles["Body"]))
            paragraph_lines = []

    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(
                    Preformatted(normalize("\n".join(code_lines)), styles["Code"])
                )
                code_lines = []
                in_code = False
            else:
                in_code = True
            index += 1
            continue
        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if stripped == r"\[":
            flush_paragraph()
            in_math = True
            math_lines = []
            index += 1
            continue
        if in_math:
            if stripped == r"\]":
                math_text = html.escape(normalize(" ".join(math_lines)), quote=False)
                story.append(
                    Table(
                        [[Paragraph(math_text, styles["Math"])]],
                        colWidths=[available_width * 0.9],
                        hAlign="CENTER",
                        style=TableStyle(
                            [
                                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7FA")),
                                ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#BCCCDC")),
                                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                                ("TOPPADDING", (0, 0), (-1, -1), 6),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                            ]
                        ),
                    )
                )
                in_math = False
                math_lines = []
            else:
                math_lines.append(stripped)
            index += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = min(len(heading.group(1)), 4)
            story.append(
                Paragraph(
                    inline_markup(heading.group(2)),
                    styles[f"Heading{level}"],
                )
            )
            index += 1
            continue

        image_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", stripped)
        if image_match:
            flush_paragraph()
            alt, target = image_match.groups()
            image_path = (path.parent / target).resolve()
            if image_path.exists():
                story.append(Spacer(1, 4))
                story.append(
                    image_flowable(
                        image_path,
                        max_width=available_width,
                        max_height=135 * mm,
                    )
                )
                if alt:
                    story.append(Paragraph(inline_markup(alt), styles["Caption"]))
            else:
                story.append(
                    Paragraph(
                        f"<i>Image unavailable in package: {html.escape(target)}</i>",
                        styles["Small"],
                    )
                )
            index += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            table_lines = []
            while (
                index < len(lines)
                and lines[index].strip().startswith("|")
                and lines[index].strip().endswith("|")
            ):
                table_lines.append(lines[index].strip())
                index += 1
            rows = [
                [cell.strip() for cell in table_line.strip("|").split("|")]
                for table_line in table_lines
            ]
            if len(rows) >= 2 and all(
                re.fullmatch(r":?-{3,}:?", cell.replace(" ", ""))
                for cell in rows[1]
            ):
                rows.pop(1)
            story.append(table_flowable(rows, styles, available_width))
            story.append(Spacer(1, 7))
            continue

        if re.fullmatch(r"---+", stripped):
            flush_paragraph()
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.6,
                    color=colors.HexColor("#BCCCDC"),
                    spaceBefore=5,
                    spaceAfter=7,
                )
            )
            index += 1
            continue

        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        if bullet:
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(bullet.group(1)),
                    styles["Bullet"],
                    bulletText="•",
                )
            )
            index += 1
            continue

        numbered = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
        if numbered:
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(numbered.group(2)),
                    styles["Numbered"],
                    bulletText=f"{numbered.group(1)}.",
                )
            )
            index += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            story.append(
                Paragraph(inline_markup(stripped.lstrip("> ")), styles["Callout"])
            )
            index += 1
            continue

        if not stripped:
            flush_paragraph()
            index += 1
            continue

        paragraph_lines.append(stripped)
        index += 1

    flush_paragraph()
    if code_lines:
        story.append(Preformatted("\n".join(code_lines), styles["Code"]))
    return story


def cover_story(styles, available_width: float):
    story = [Spacer(1, 14 * mm)]
    story.append(
        Paragraph(
            "Development of a Multimodal Non-Destructive<br/>"
            "Avocado Ripeness Characterization System",
            ParagraphStyle(
                "CoverTitle",
                fontName="ProposalSans-Bold",
                fontSize=25,
                leading=30,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#102A43"),
                spaceAfter=12,
            ),
        )
    )
    story.append(
        Paragraph(
            "Optical spectroscopy, embedded sensing, machine learning, "
            "and scientific machine learning",
            ParagraphStyle(
                "CoverSubtitle",
                fontName="ProposalSans",
                fontSize=13,
                leading=18,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#1F5A7A"),
                spaceAfter=13,
            ),
        )
    )
    overview = ROOT / "figures" / "prototype-system-overview.png"
    if overview.exists():
        story.append(
            image_flowable(
                overview,
                max_width=available_width,
                max_height=92 * mm,
            )
        )
        story.append(Spacer(1, 5))

    headline_data = [
        [
            Paragraph("<b>478</b><br/>independent fruits", styles["Body"]),
            Paragraph("<b>14,710</b><br/>audited RGB images", styles["Body"]),
            Paragraph("<b>44</b><br/>BOM line items", styles["Body"]),
            Paragraph("<b>US$723.62</b><br/>MVP planning total", styles["Body"]),
        ]
    ]
    highlights = Table(
        headline_data,
        colWidths=[available_width / 4] * 4,
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF4F4")),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#9FB3C8")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BCCCDC")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        ),
    )
    story.append(highlights)
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "<b>Prepared 30 July 2026</b><br/>"
            "For discussion with collaborators, supervisors, "
            "and prospective laboratory or funding partners",
            ParagraphStyle(
                "CoverMeta",
                parent=styles["Body"],
                alignment=TA_CENTER,
                fontSize=9.5,
                leading=14,
            ),
        )
    )
    story.append(
        Paragraph(
            "<b>Evidence boundary.</b> Results reproduced here are internal "
            "fruit-grouped analyses of one public study. Hardware, equations, "
            "experimental endpoints, and scientific-ML methods are proposed "
            "until prospectively validated.",
            styles["Callout"],
        )
    )
    story.append(PageBreak())
    story.append(Paragraph("Contents", styles["Heading1"]))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOC1",
            fontName="ProposalSans-Bold",
            fontSize=9.5,
            leading=14,
            leftIndent=0,
            firstLineIndent=0,
            textColor=colors.HexColor("#102A43"),
            spaceBefore=4,
        ),
        ParagraphStyle(
            "TOC2",
            fontName="ProposalSans",
            fontSize=8.2,
            leading=11,
            leftIndent=12,
            firstLineIndent=0,
            textColor=colors.HexColor("#334E68"),
        ),
        ParagraphStyle(
            "TOC3",
            fontName="ProposalSans",
            fontSize=7.4,
            leading=9.5,
            leftIndent=24,
            textColor=colors.HexColor("#486581"),
        ),
    ]
    story.append(toc)
    story.append(PageBreak())
    return story


def main() -> None:
    register_fonts()
    missing = [path for path in SOURCES if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Required proposal sources are missing:\n"
            + "\n".join(str(path) for path in missing)
        )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    margin_left = 18 * mm
    margin_right = 18 * mm
    margin_top = 20 * mm
    margin_bottom = 18 * mm
    available_width = A4[0] - margin_left - margin_right

    doc = ProposalDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=margin_left,
        rightMargin=margin_right,
        topMargin=margin_top,
        bottomMargin=margin_bottom,
        title="Multimodal Non-Destructive Avocado Ripeness Characterization",
        author="Research collaboration proposal",
        subject="Avocado sensing, machine learning, and scientific machine learning",
    )
    story = cover_story(styles, available_width)
    for source_index, source in enumerate(SOURCES):
        if source_index:
            story.append(PageBreak())
        story.extend(parse_markdown(source, styles, available_width))

    doc.multiBuild(story, canvasmaker=NumberedCanvas)
    print(OUTPUT)


if __name__ == "__main__":
    main()
