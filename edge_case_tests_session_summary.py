from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/nfs/s-l011/local/vol02/n/nkrchak/Documents/MIATT/hw04-noah-krchak/edge_case_tests_session_summary.pdf"

COMMIT_HASH = "1e00bebc1e86f7d8a665f26f5fc7cce13018ec56"
COMMIT_SHORT = "1e00beb"
COMMIT_MSG = "ENH: Added 26 edge-case CTest unit tests across all five filter programs"

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
commit_style = ParagraphStyle(
    "Commit", parent=styles["Normal"],
    fontSize=9, leading=13, spaceAfter=6,
    backColor=colors.HexColor("#eef4ff"),
    leftIndent=10, rightIndent=10,
    borderPad=6,
    fontName="Courier",
    textColor=colors.HexColor("#1a1a2e"),
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

def commit_block(text):
    return Paragraph(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), commit_style)

def bullet(text):
    return Paragraph(f"&#x2022;&nbsp;&nbsp;{text}", bullet_style)

story = []

# Title block
story.append(Paragraph("Session Summary — HW04 Edge-Case Unit Tests", title_style))
story.append(Paragraph(
    "Project: ECE:5490 HW04 &nbsp;|&nbsp; Date: 2026-04-16 &nbsp;|&nbsp; User: nkrchak",
    subtitle_style,
))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a1a2e"), spaceAfter=10))

# Commit reference block
story.append(body("<b>Git Commit Reference</b>"))
story.append(commit_block(
    f"Commit: {COMMIT_HASH}\n"
    f"Short:  {COMMIT_SHORT}\n"
    f"Branch: main\n"
    f"Repo:   github.com/uiowaMIATT2026/hw04-noah-krchak\n"
    f"Msg:    {COMMIT_MSG}"
))
story.append(Spacer(1, 4))

# ── 1. USER PROMPT ────────────────────────────────────────────────────────────
story += section("1. User Prompt")
story.append(body(
    "Following the initial unit-test session (commit <font name='Courier'>45b1dc3</font>), "
    "the user asked the AI to suggest and then implement edge-case tests for each of the five "
    "filter programs, using the negative-sigma example as a starting point."
))
story.append(Spacer(1, 4))
story.append(code(
    'What unit tests could I add to test edge-cases for each of the\n'
    'algorithms such as inputting a negative sigma for the low pass\n'
    'gaussian filter?'
))
story.append(Spacer(1, 6))
story.append(body(
    "After the AI listed the suggested edge cases in a table, the user issued a follow-up "
    "prompt to implement all of them:"
))
story.append(Spacer(1, 4))
story.append(code(
    'Yes, implement each of these tests and state what each test is\n'
    'testing in the comments'
))

# ── 2. AI QUESTIONS ───────────────────────────────────────────────────────────
story += section("2. Questions Asked by the AI")
story.append(body(
    "No clarifying questions were asked. All information needed to propose and implement "
    "the edge-case tests was available from the existing source files, XML descriptors, "
    "and the ITK documentation embedded in the exception messages produced during probing."
))

# ── 3. AI ACTIONS ─────────────────────────────────────────────────────────────
story += section("3. What the AI Did")

story.append(body("<b>Step 1 — Proposed edge cases</b>"))
story.append(bullet("Analysed each algorithm's filter pipeline and XML parameter constraints."))
story.append(bullet("Identified four categories of edge case: invalid parameter values, "
                    "boundary constraint values, degenerate-but-legal inputs, and reversed "
                    "parameter ordering."))
story.append(bullet("Presented the proposed tests to the user in a structured table before "
                    "writing any code."))

story.append(Spacer(1, 6))
story.append(body("<b>Step 2 — Probed actual ITK behaviour before writing tests</b>"))
story.append(body(
    "Rather than assuming what each program would do, the AI ran each candidate edge-case "
    "directly against the built executables to record the true exit code and stderr output. "
    "Key findings:"
))
story.append(bullet(
    "<b>GaussianLPF / DOG — negative or zero sigma:</b> ITK's "
    "<font name='Courier'>RecursiveGaussianImageFilter</font> throws "
    "<i>\"Sigma must be greater than zero\"</i> → EXIT_FAILURE confirmed."
))
story.append(bullet(
    "<b>SimpleThreshold — inverted range:</b> ITK's "
    "<font name='Courier'>BinaryThresholdImageFilter</font> throws "
    "<i>\"Lower threshold cannot be greater than upper threshold\"</i> → EXIT_FAILURE confirmed."
))
story.append(bullet(
    "<b>GradientAD / CurvatureAD — negative conductance, zero/negative timeStep, "
    "unstable timeStep, zero iterations:</b> ITK does not validate any of these; it "
    "either issues a stderr stability warning or silently produces degenerate output. "
    "All cases return EXIT_SUCCESS."
))

story.append(Spacer(1, 6))
story.append(body("<b>Step 3 — Implemented tests with explanatory comments</b>"))
story.append(bullet("Added 4 edge-case tests to <b>src/SimpleThreshold/CMakeLists.txt</b>."))
story.append(bullet("Added 4 edge-case tests to <b>src/GaussianLPF/CMakeLists.txt</b>."))
story.append(bullet("Added 4 edge-case tests to <b>src/DOG/CMakeLists.txt</b>."))
story.append(bullet("Added 7 edge-case tests to <b>src/GradientAD/CMakeLists.txt</b>."))
story.append(bullet("Added 7 edge-case tests to <b>src/CurvatureAD/CMakeLists.txt</b>."))
story.append(bullet(
    "Each test has an inline comment explaining the specific ITK behaviour being "
    "exercised and why the expected exit code is what it is."
))

story.append(Spacer(1, 6))
story.append(body("<b>Step 4 — Verification and commit</b>"))
story.append(bullet("Re-ran <code>cmake ..</code> to register the 26 new tests (42 total)."))
story.append(bullet("Ran <code>ctest --output-on-failure</code>: <b>42/42 tests passed</b>."))
story.append(bullet(
    f"Committed and pushed to GitHub as <font name='Courier'>{COMMIT_SHORT}</font>."
))

# ── 4. TEST TABLE ─────────────────────────────────────────────────────────────
story += section("4. Edge-Case Tests Added (26 New Tests)")

header = ["#", "Test Name", "Edge Case Tested", "Expected"]
rows = [
    header,
    # SimpleThreshold
    ["1",  "SimpleThreshold_InvertedRange",       "lowThreshold > highThreshold",                "FAIL"],
    ["2",  "SimpleThreshold_SingleValueRange",    "lowThreshold == highThreshold (single value)", "PASS"],
    ["3",  "SimpleThreshold_InsideEqualsOutside", "insideValue == outsideValue (uniform output)", "PASS"],
    ["4",  "SimpleThreshold_FullRange",           "Range [0,255] maps all pixels to insideValue", "PASS"],
    # GaussianLPF
    ["5",  "GaussianLPF_NegativeSigma",           "sigma = -1.0 (ITK throws)",                   "FAIL"],
    ["6",  "GaussianLPF_ZeroSigma",               "sigma = 0.0 (ITK throws)",                    "FAIL"],
    ["7",  "GaussianLPF_BoundaryMinSigma",        "sigma = 0.1 (XML minimum boundary)",           "PASS"],
    ["8",  "GaussianLPF_BoundaryMaxSigma",        "sigma = 5.0 (XML maximum boundary)",           "PASS"],
    # DOG
    ["9",  "DOG_NegativeSigma1",                  "sigma1 = -1.0 (ITK throws)",                  "FAIL"],
    ["10", "DOG_ZeroSigma2",                      "sigma2 = 0.0 (ITK throws)",                   "FAIL"],
    ["11", "DOG_ReversedSigmas",                  "sigma1 > sigma2 (inverted edge response)",     "PASS"],
    ["12", "DOG_CloseSigmas",                     "sigma1=2.5, sigma2=2.6 (faint edge response)", "PASS"],
    # GradientAD
    ["13", "GradientAD_NegativeConductance",      "conductance = -1.0 (ITK silent, bad output)",  "PASS"],
    ["14", "GradientAD_ZeroTimeStep",             "timeStep = 0.0 (no-op per iteration)",         "PASS"],
    ["15", "GradientAD_NegativeTimeStep",         "timeStep = -0.1 (ITK silent, reverse diffusion)", "PASS"],
    ["16", "GradientAD_UnstableTimeStep",         "timeStep = 0.13 > CFL limit 0.0625 (ITK warns)", "PASS"],
    ["17", "GradientAD_ZeroIterations",           "iterations = 0 (loop never executes)",         "PASS"],
    ["18", "GradientAD_BoundaryMinIterations",    "iterations = 1 (XML minimum boundary)",        "PASS"],
    ["19", "GradientAD_BoundaryMaxIterations",    "iterations = 20 (XML maximum boundary)",       "PASS"],
    # CurvatureAD
    ["20", "CurvatureAD_NegativeConductance",     "conductance = -1.0 (ITK silent, bad output)",  "PASS"],
    ["21", "CurvatureAD_ZeroTimeStep",            "timeStep = 0.0 (no-op per iteration)",         "PASS"],
    ["22", "CurvatureAD_NegativeTimeStep",        "timeStep = -0.1 (ITK silent, reverse diffusion)", "PASS"],
    ["23", "CurvatureAD_UnstableTimeStep",        "timeStep = 0.13 > CFL limit 0.0625 (ITK warns)", "PASS"],
    ["24", "CurvatureAD_ZeroIterations",          "iterations = 0 (loop never executes)",         "PASS"],
    ["25", "CurvatureAD_BoundaryMinIterations",   "iterations = 1 (XML minimum boundary)",        "PASS"],
    ["26", "CurvatureAD_BoundaryMaxIterations",   "iterations = 20 (XML maximum boundary)",       "PASS"],
]

col_widths = [0.28*inch, 2.55*inch, 2.85*inch, 0.65*inch]
tbl = Table(rows, colWidths=col_widths, repeatRows=1)

def row_bg(i):
    return colors.white if i % 2 == 0 else colors.HexColor("#f0f4ff")

fail_red = colors.HexColor("#ffe8e8")
style_cmds = [
    ("BACKGROUND",    (0, 0),  (-1, 0),  colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR",     (0, 0),  (-1, 0),  colors.white),
    ("FONTNAME",      (0, 0),  (-1, 0),  "Helvetica-Bold"),
    ("FONTSIZE",      (0, 0),  (-1, 0),  9),
    ("FONTNAME",      (0, 1),  (-1, -1), "Helvetica"),
    ("FONTSIZE",      (0, 1),  (-1, -1), 8),
    ("GRID",          (0, 0),  (-1, -1), 0.4, colors.HexColor("#bbbbbb")),
    ("VALIGN",        (0, 0),  (-1, -1), "MIDDLE"),
    ("TOPPADDING",    (0, 0),  (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0),  (-1, -1), 4),
    ("LEFTPADDING",   (0, 0),  (-1, -1), 5),
]
# Alternating row backgrounds
for i in range(1, len(rows)):
    bg = fail_red if rows[i][-1] == "FAIL" else row_bg(i)
    style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

tbl.setStyle(TableStyle(style_cmds))
story.append(tbl)
story.append(Spacer(1, 6))
story.append(body(
    "<i>Rows highlighted in red indicate tests marked WILL_FAIL TRUE — "
    "the program is expected to return EXIT_FAILURE for that input.</i>"
))

# ── 5. AI RESPONSE SUMMARY ───────────────────────────────────────────────────
story += section("5. AI Response Summary")
story.append(body(
    "The AI first presented the proposed edge cases as a structured table and explained "
    "the rationale for each. After the user confirmed, it probed the actual ITK behaviour "
    "by running the built executables directly before writing a single test, ensuring that "
    "<font name='Courier'>WILL_FAIL</font> flags were set accurately rather than assumed."
))
story.append(Spacer(1, 4))
story.append(body(
    "All 42 tests in the suite (16 original + 26 new) passed. Total CTest run time was "
    "approximately 9.5 minutes, dominated by the GradientAD and CurvatureAD 20-iteration "
    "boundary tests (~110 s and ~120 s respectively)."
))
story.append(Spacer(1, 4))
story.append(body("The complete test suite can be re-run with:"))
story.append(code("cd cmake-build-debug && ctest --output-on-failure"))

doc.build(story)
print(f"PDF written to {OUTPUT}")
