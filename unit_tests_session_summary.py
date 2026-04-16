from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/nfs/s-l011/local/vol02/n/nkrchak/Documents/MIATT/hw04-noah-krchak/unit_tests_session_summary.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.85*inch,
    leftMargin=0.85*inch,
    topMargin=0.85*inch,
    bottomMargin=0.85*inch,
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title", parent=styles["Title"],
    fontSize=18, spaceAfter=6, textColor=colors.HexColor("#1a1a2e"),
)
subtitle_style = ParagraphStyle(
    "Subtitle", parent=styles["Normal"],
    fontSize=10, spaceAfter=16, textColor=colors.HexColor("#555555"),
    alignment=TA_CENTER,
)
section_style = ParagraphStyle(
    "Section", parent=styles["Heading2"],
    fontSize=13, spaceBefore=14, spaceAfter=6,
    textColor=colors.HexColor("#1a1a2e"),
    borderPad=2,
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontSize=9.5, leading=14, spaceAfter=6,
)
code_style = ParagraphStyle(
    "Code", parent=styles["Code"],
    fontSize=8, leading=12, spaceAfter=4,
    backColor=colors.HexColor("#f4f4f4"),
    leftIndent=12, rightIndent=12,
    borderPad=4,
    fontName="Courier",
)
bullet_style = ParagraphStyle(
    "Bullet", parent=body_style,
    leftIndent=18, bulletIndent=6, spaceAfter=3,
)

def section(title):
    return [
        Spacer(1, 6),
        Paragraph(title, section_style),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc"), spaceAfter=6),
    ]

def body(text):
    return Paragraph(text, body_style)

def code(text):
    return Paragraph(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)

def bullet(text):
    return Paragraph(f"&#x2022;&nbsp;&nbsp;{text}", bullet_style)

story = []

# Title block
story.append(Paragraph("Session Summary — HW04 Unit Tests", title_style))
story.append(Paragraph(
    "Project: ECE:5490 HW04 &nbsp;|&nbsp; Date: 2026-04-16 &nbsp;|&nbsp; User: nkrchak",
    subtitle_style,
))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e"), spaceAfter=10))

# ── 1. USER PROMPT ────────────────────────────────────────────────────────────
story += section("1. User Prompt")
story.append(body(
    "The user asked Claude to read the repository and the <b>README.md</b>, then generate "
    "unit tests for each program using the example parameters provided in the README."
))
story.append(Spacer(1, 4))
story.append(code(
    'Please read this repository and the README.md then generate unit\n'
    'tests for each program based on the example parameters given by\n'
    'the README.md'
))

# ── 2. AI QUESTIONS ───────────────────────────────────────────────────────────
story += section("2. Questions Asked by the AI")
story.append(body(
    "No clarifying questions were asked. All information required to generate the tests "
    "was available in the repository files, the README, and the data directory "
    "at <i>/nfsscratch/opt/ece5490/data</i>."
))

# ── 3. AI ACTIONS ─────────────────────────────────────────────────────────────
story += section("3. What the AI Did")

story.append(body("<b>Step 1 — Repository exploration</b>"))
story.append(bullet("Read <b>README.md</b> to extract example CLI invocations and expected behaviour for all five programs."))
story.append(bullet("Read each <b>.cxx</b> source file to understand filter pipelines, pixel types, and error paths."))
story.append(bullet("Read each <b>.xml</b> SEM descriptor to obtain exact flag names, types, defaults, and constraints."))
story.append(bullet("Read each <b>CMakeLists.txt</b> to understand how executables are named and built."))
story.append(bullet("Confirmed the five pre-built executables existed under <i>cmake-build-debug/src/</i>."))
story.append(bullet("Verified test image availability at <i>/nfsscratch/opt/ece5490/data/noisy/</i>."))

story.append(Spacer(1, 6))
story.append(body("<b>Step 2 — Code changes</b>"))
story.append(bullet(
    "Added <code>enable_testing()</code> to the root <b>CMakeLists.txt</b> to activate CTest."
))
story.append(bullet(
    "Added three CTest tests to <b>src/SimpleThreshold/CMakeLists.txt</b>."
))
story.append(bullet(
    "Added three CTest tests to <b>src/GaussianLPF/CMakeLists.txt</b>."
))
story.append(bullet(
    "Added four CTest tests to <b>src/DOG/CMakeLists.txt</b> (including an equal-sigma rejection test)."
))
story.append(bullet(
    "Added three CTest tests to <b>src/GradientAD/CMakeLists.txt</b>."
))
story.append(bullet(
    "Added three CTest tests to <b>src/CurvatureAD/CMakeLists.txt</b>."
))

story.append(Spacer(1, 6))
story.append(body("<b>Step 3 — Verification</b>"))
story.append(bullet("Re-ran <code>cmake ..</code> inside <i>cmake-build-debug/</i> to pick up the new tests."))
story.append(bullet("Confirmed all 16 tests registered with <code>ctest -N</code>."))
story.append(bullet("Ran <code>ctest --output-on-failure</code>: <b>16/16 tests passed</b>."))

# ── 4. TEST TABLE ─────────────────────────────────────────────────────────────
story += section("4. Tests Generated (16 Total)")

header = ["#", "Test Name", "What It Verifies"]
rows = [
    header,
    ["1",  "SimpleThreshold_ExampleParams", "README params (low=50, high=100, outside=150, inside=200) → EXIT_SUCCESS"],
    ["2",  "SimpleThreshold_OutputCreated",  "Output .nii.gz file exists after the run"],
    ["3",  "SimpleThreshold_MissingInput",   "Non-existent input path → EXIT_FAILURE"],
    ["4",  "GaussianLPF_ExampleParams",      "README params (sigma=2.5) → EXIT_SUCCESS"],
    ["5",  "GaussianLPF_OutputCreated",      "Output .nii.gz file exists after the run"],
    ["6",  "GaussianLPF_MissingInput",       "Non-existent input path → EXIT_FAILURE"],
    ["7",  "DOG_ExampleParams",              "README params (sigma1=2.5, sigma2=3.5) → EXIT_SUCCESS"],
    ["8",  "DOG_OutputCreated",              "Output .nii.gz file exists after the run"],
    ["9",  "DOG_EqualSigmas",               "sigma1 == sigma2 is rejected → EXIT_FAILURE"],
    ["10", "DOG_MissingInput",               "Non-existent input path → EXIT_FAILURE"],
    ["11", "GradientAD_ExampleParams",       "README params (cond=2.0, dt=0.1, iter=5) → EXIT_SUCCESS"],
    ["12", "GradientAD_OutputCreated",       "Output .nii.gz file exists after the run"],
    ["13", "GradientAD_MissingInput",        "Non-existent input path → EXIT_FAILURE"],
    ["14", "CurvatureAD_ExampleParams",      "README params (cond=2.0, dt=0.1, iter=5) → EXIT_SUCCESS"],
    ["15", "CurvatureAD_OutputCreated",      "Output .nii.gz file exists after the run"],
    ["16", "CurvatureAD_MissingInput",       "Non-existent input path → EXIT_FAILURE"],
]

col_widths = [0.3*inch, 2.6*inch, 3.6*inch]
tbl = Table(rows, colWidths=col_widths, repeatRows=1)
tbl.setStyle(TableStyle([
    ("BACKGROUND",   (0, 0), (-1, 0),  colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
    ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
    ("FONTSIZE",     (0, 0), (-1, 0),  9),
    ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE",     (0, 1), (-1, -1), 8.5),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f4ff")]),
    ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
    ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING",   (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
    ("LEFTPADDING",  (0, 0), (-1, -1), 5),
]))
story.append(tbl)

# ── 5. AI RESPONSE SUMMARY ───────────────────────────────────────────────────
story += section("5. AI Response Summary")
story.append(body(
    "Claude confirmed that all 16 CTest tests passed (0 failures). It provided a Markdown "
    "table in-chat summarising every test name and what it checks, and noted that the suite "
    "can be re-run at any time from the build directory with:"
))
story.append(Spacer(1, 4))
story.append(code("ctest --output-on-failure"))
story.append(Spacer(1, 4))
story.append(body(
    "The two iterative diffusion tests (<i>GradientAD</i> and <i>CurvatureAD</i>) each took "
    "approximately 28–30 seconds due to the 5-iteration filter pass over a full 3-D volume. "
    "All other tests completed in under 1 second."
))

doc.build(story)
print(f"PDF written to {OUTPUT}")
