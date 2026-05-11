from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)

WIDTH = 1440
HEIGHT = 900
BG = "#091321"
PANEL = "#131f31"
CARD = "#1a2940"
BORDER = "#294764"
TEXT = "#f3efe1"
SUB = "#b8c7dc"
ACCENT = "#8bc5ff"
WARN = "#ffd76d"


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


TITLE = font(54, True)
SECTION = font(18, False)
BODY = font(26, False)
CARD_TITLE = font(18, False)
CARD_VALUE = font(34, True)
CARD_BODY = font(19, False)


def wrapped(draw, text, xy, wrap_width, font_obj, fill, line_gap=10):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=font_obj) <= wrap_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    x, y = xy
    line_height = font_obj.size + line_gap
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += line_height


def shell():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((30, 30, WIDTH - 30, HEIGHT - 30), 28, fill=PANEL, outline=BORDER, width=2)
    return image, draw


def hero():
    image, draw = shell()
    draw.text((90, 82), "SECRET ROTATION SCHEDULER", font=SECTION, fill=ACCENT)
    wrapped(draw, "Turn credential decay into a clear rotation decision.", (90, 130), 1100, TITLE, TEXT, 8)
    wrapped(draw, "Stale windows, expiring secrets, break-glass exposure, and owner coverage in one Python service.", (90, 270), 1100, BODY, SUB, 8)
    cards = [
        ("TRACKED SECRETS", "3", "Modeled inventory threads"),
        ("EXPIRING SOON", "2", "Inside the 14-day buffer"),
        ("STALE ROTATIONS", "1", "Already beyond window"),
        ("BREAK GLASS", "1", "Elevated governance lane"),
    ]
    x = 90
    for title, value, body in cards:
        draw.rounded_rectangle((x, 360, x + 285, 555), 22, fill=CARD, outline=BORDER, width=2)
        draw.text((x + 24, 388), title, font=CARD_TITLE, fill=SUB)
        draw.text((x + 24, 430), value, font=CARD_VALUE, fill=TEXT)
        wrapped(draw, body, (x + 24, 488), 230, CARD_BODY, SUB, 6)
        x += 305
    draw.rounded_rectangle((90, 620, WIDTH - 90, 800), 24, fill=CARD, outline=BORDER, width=2)
    draw.text((120, 652), "CURRENT DECISION", font=CARD_TITLE, fill="#ffbfdc")
    wrapped(draw, "Rotate the billing export secret now and assign a backup owner before the finance-close path locks in.", (120, 694), 1120, font(38, True), TEXT, 8)
    image.save(OUT / "01-hero.png")


def lanes():
    image, draw = shell()
    draw.text((90, 82), "OWNER LANES", font=SECTION, fill=ACCENT)
    wrapped(draw, "Security hygiene gets cleaner when the rotation lanes are explicit.", (90, 130), 1080, TITLE, TEXT, 8)
    cards = [
        ("PLATFORM SECURITY", "Immediate rotation and backup-owner assignment", "Prod export key"),
        ("IDENTITY SYSTEMS", "Break-glass cert verification", "Prod identity cert"),
        ("GROWTH SYSTEMS", "Normal scheduler cadence", "Stage token"),
    ]
    x = 110
    for title, body, tag in cards:
        draw.rounded_rectangle((x, 300, x + 360, 620), 24, fill=CARD, outline=BORDER, width=2)
        draw.text((x + 28, 332), title, font=CARD_TITLE, fill=ACCENT)
        wrapped(draw, body, (x + 28, 402), 300, font(30, True), TEXT, 8)
        draw.text((x + 28, 544), tag, font=font(22, False), fill=WARN)
        x += 390
    image.save(OUT / "02-lanes.png")


def decision():
    image, draw = shell()
    draw.text((90, 82), "ROTATION DECISION", font=SECTION, fill=ACCENT)
    wrapped(draw, "One secret, one score, one action path.", (90, 130), 960, TITLE, TEXT, 8)
    draw.rounded_rectangle((90, 290, 770, 780), 24, fill=CARD, outline=BORDER, width=2)
    draw.text((120, 322), "SEC-7004 · BILLING EXPORT", font=CARD_TITLE, fill=ACCENT)
    draw.text((120, 390), "Status: escalate", font=font(38, True), fill=TEXT)
    draw.text((120, 450), "Decision: rotate-now", font=font(24, False), fill=SUB)
    draw.text((120, 492), "Recommended lane: incident-command", font=font(24, False), fill=SUB)
    draw.text((120, 552), "Key risks", font=font(26, True), fill=TEXT)
    wrapped(draw, "The secret is stale, near expiration, and missing a backup owner.", (120, 596), 560, CARD_BODY, SUB, 6)

    draw.rounded_rectangle((810, 290, WIDTH - 90, 780), 24, fill=CARD, outline=BORDER, width=2)
    draw.text((840, 322), "IMMEDIATE ACTION", font=CARD_TITLE, fill="#ffbfdc")
    wrapped(draw, "Assign a named backup owner, rotate the production key now, and freeze dependent deploys until proof is captured.", (840, 382), 470, font(30, True), TEXT, 8)
    draw.text((840, 560), "Stabilizers", font=font(26, True), fill=TEXT)
    wrapped(draw, "A next-step sequence already exists, so the issue is ownership and timing, not complete ambiguity.", (840, 604), 470, CARD_BODY, SUB, 6)
    image.save(OUT / "03-decision.png")


def proof():
    image, draw = shell()
    draw.text((90, 82), "VALIDATION PROOF", font=SECTION, fill=ACCENT)
    wrapped(draw, "Pytest, API routes, and CLI output in one proof layer.", (90, 130), 1060, TITLE, TEXT, 8)
    draw.rounded_rectangle((90, 300, 760, 790), 24, fill="#07101c", outline=BORDER, width=2)
    proof_lines = [
        "> pytest",
        "test_critical_secret_escalates ... ok",
        "test_summary_counts_inventory ... ok",
        "",
        "> python -m app.cli",
        "sec-7004: rotate-now (escalate) -> incident-command",
        "sec-7011: watch (prioritize) -> identity-systems",
        "sec-7018: stable (schedule) -> growth-systems",
    ]
    y = 336
    mono = font(24, False)
    for line in proof_lines:
        draw.text((120, y), line, font=mono, fill="#c8f7a5" if line.startswith(">") else SUB)
        y += 34

    draw.rounded_rectangle((810, 300, WIDTH - 90, 790), 24, fill=CARD, outline=BORDER, width=2)
    draw.text((840, 332), "WHY THIS COUNTS", font=CARD_TITLE, fill=ACCENT)
    wrapped(draw, "The scheduler shows practical security operations logic and gives the portfolio another Python backend that feels rooted in real hygiene work.", (840, 390), 470, font(28, True), TEXT, 8)
    image.save(OUT / "04-proof.png")


if __name__ == "__main__":
    hero()
    lanes()
    decision()
    proof()
