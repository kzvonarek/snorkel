"""Generate the three static demo PMF reports served by the frontend."""

from pathlib import Path
from shutil import copy2

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf"
PUBLIC = ROOT / "frontend" / "public" / "reports"

TOPICS = [
    {
        "slug": "orbit-note", "name": "Orbit Note", "category": "NEW TECH PRODUCT", "color": "#4B5FA8", "fit": 78,
        "tagline": "An AI meeting puck that turns room audio into decisions, owners, and follow-ups.",
        "question": "Will hybrid teams trust and pay for an always-on AI meeting device?",
        "signals": [("Workflow value", 86), ("Pilot intent", 67), ("Trust readiness", 54), ("Budget fit", 63)],
        "segments": [("Product and operations", "Strong pull", "Decision logs and action handoffs solve a frequent coordination problem."), ("Employees", "Conditional", "Visible hardware helps, but consent and source-linked summaries are expected."), ("IT and security", "Blocked", "Retention, deletion, regional processing, SCIM, and audit logs are required.")],
        "objections": ["Recording consent and visible privacy controls", "Enterprise retention, deletion, and regional processing", "Hardware cost compared with software meeting bots"],
        "quotes": ["The decision log is immediately useful. I spend Mondays reconstructing who promised what.", "Always-on audio creates a consent problem before it creates a productivity win.", "I would pilot this in three rooms if every claim links back to the moment it was said."],
        "recommendation": "Pilot in three hybrid meeting rooms with raw-audio storage disabled. Gate expansion on action-item precision, consent comprehension, and administrator controls.",
    },
    {
        "slug": "emberwild", "name": "Emberwild", "category": "NEW VIDEO GAME", "color": "#8E6B4E", "fit": 81,
        "tagline": "A four-player survival game where seasons reshape the map and alliances determine the ending.",
        "question": "Can a social survival game retain both coordinated groups and solo players?",
        "signals": [("Concept appeal", 89), ("Wishlist intent", 78), ("Group retention", 82), ("Solo readiness", 51)],
        "segments": [("Co-op groups", "Strong pull", "Persistent settlements and consequential seasonal choices create return motivation."), ("Creators", "Strong pull", "Map transformations and alliance outcomes produce compelling public moments."), ("Solo and time-limited", "At risk", "Catch-up, no-voice matchmaking, and reduced grind determine accessibility.")],
        "objections": ["Seasonal progress may punish time-limited players", "Solo and no-voice matchmaking need first-class support", "Resource grind could overwhelm the social differentiation"],
        "quotes": ["A shared settlement that remembers our choices gives the group a reason to return.", "I cannot lose a whole season because I missed two evenings.", "I would wishlist after a demo that proves the social systems create stories, not just grind."],
        "recommendation": "Ship a public co-op demo centered on one seasonal transformation. Measure group return intent while testing catch-up, solo companions, and reduced midgame resource chores.",
    },
    {
        "slug": "harbor-commons", "name": "Harbor Commons", "category": "NEW APARTMENT COMMUNITY", "color": "#3B7355", "fit": 73,
        "tagline": "A transit-oriented apartment community with flexible units, shared workspaces, and family services.",
        "question": "Which amenities and lease design create enough value to support premium rents?",
        "signals": [("Location value", 88), ("Tour intent", 71), ("Amenity fit", 68), ("Price trust", 49)],
        "segments": [("Professionals", "Strong pull", "Transit, secure bike storage, and bookable quiet rooms improve monthly value."), ("Families and downsizers", "Conditional", "Storage, acoustics, guest space, and dependable services matter more than spectacle."), ("Budget renters", "At risk", "Mandatory amenity and surprise monthly fees undermine trust before a tour.")],
        "objections": ["Total monthly cost and mandatory amenity fees", "Family storage, acoustics, and dependable childcare", "Late-night transit safety and building access controls"],
        "quotes": ["Train access plus secure bike storage would let me drop a car payment.", "Publish the complete monthly cost before I tour.", "Ground-floor local retail makes the place feel like a neighborhood."],
        "recommendation": "Test demand with transparent all-in pricing and three amenity bundles. Prioritize quiet work rooms, mobility infrastructure, safety, and functional family layouts.",
    },
]


class SignalBar(Flowable):
    def __init__(self, label, value, color):
        super().__init__(); self.label = label; self.value = value; self.color = colors.HexColor(color); self.width = 440; self.height = 28

    def draw(self):
        self.canv.setFont("Helvetica", 9); self.canv.setFillColor(colors.HexColor("#505C78")); self.canv.drawString(0, 17, self.label)
        self.canv.setFillColor(colors.HexColor("#E8EAF1")); self.canv.roundRect(115, 12, 270, 8, 4, fill=1, stroke=0)
        self.canv.setFillColor(self.color); self.canv.roundRect(115, 12, 270 * self.value / 100, 8, 4, fill=1, stroke=0)
        self.canv.setFillColor(colors.HexColor("#1A1F30")); self.canv.setFont("Helvetica-Bold", 9); self.canv.drawRightString(430, 17, f"{self.value}%")


def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor("#E2E6F0")); canvas.line(0.65 * inch, 0.55 * inch, 7.85 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(colors.HexColor("#7882A0")); canvas.drawString(0.65 * inch, 0.35 * inch, "SNORKEL - CURATED DEMO SIMULATION")
    canvas.drawRightString(7.85 * inch, 0.35 * inch, f"PAGE {doc.page}"); canvas.restoreState()


def build(topic):
    OUTPUT.mkdir(parents=True, exist_ok=True); PUBLIC.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / f"{topic['slug']}-pmf-report.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter, rightMargin=0.7*inch, leftMargin=0.7*inch, topMargin=0.65*inch, bottomMargin=0.75*inch)
    base = getSampleStyleSheet(); accent = colors.HexColor(topic["color"])
    title = ParagraphStyle("Title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=30, leading=34, textColor=colors.HexColor("#1A1F30"), spaceAfter=12)
    h2 = ParagraphStyle("H2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=colors.HexColor("#1A1F30"), spaceBefore=8, spaceAfter=10)
    body = ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, textColor=colors.HexColor("#505C78"), spaceAfter=8)
    label = ParagraphStyle("Label", parent=body, fontName="Helvetica-Bold", fontSize=8, textColor=accent, leading=10, spaceAfter=8)
    quote = ParagraphStyle("Quote", parent=body, fontName="Helvetica-Oblique", leftIndent=14, borderColor=accent, borderWidth=2, borderPadding=(4, 0, 4, 10), spaceAfter=12)
    center = ParagraphStyle("Center", parent=body, alignment=TA_CENTER)
    story = [Paragraph(topic["category"], label), Paragraph(f"{topic['name']}<br/>PMF Simulation Report", title), Paragraph(topic["tagline"], ParagraphStyle("Lead", parent=body, fontSize=15, leading=21, textColor=colors.HexColor("#505C78"))), Spacer(1, 20)]
    score = Table([[Paragraph("FIT SIGNAL", label), Paragraph(f"<b>{topic['fit']}</b> / 100", ParagraphStyle("Score", parent=title, textColor=accent, fontSize=25))], [Paragraph("Research question", label), Paragraph(topic["question"], body)]], colWidths=[1.35*inch, 5.6*inch])
    score.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F5F6FA")),("BOX",(0,0),(-1,-1),1,colors.HexColor("#E2E6F0")),("INNERGRID",(0,0),(-1,-1),.5,colors.HexColor("#E2E6F0")),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10)]))
    story += [score, Spacer(1, 18), Paragraph("Signal overview", h2)] + [SignalBar(n,v,topic["color"]) for n,v in topic["signals"]]
    story += [Spacer(1, 14), Paragraph("Executive recommendation", h2), Paragraph(topic["recommendation"], body), PageBreak(), Paragraph("Segment response", h2)]
    rows = [[Paragraph("SEGMENT", label), Paragraph("SIGNAL", label), Paragraph("WHAT WE HEARD", label)]] + [[Paragraph(a, body), Paragraph(f"<b>{b}</b>", body), Paragraph(c, body)] for a,b,c in topic["segments"]]
    table = Table(rows, colWidths=[1.5*inch,1.15*inch,4.25*inch], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EEF0F9")),("GRID",(0,0),(-1,-1),.5,colors.HexColor("#D0D5E6")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9)]))
    story += [table, Spacer(1, 18), Paragraph("Leading objections", h2)]
    for i, item in enumerate(topic["objections"], 1): story.append(Paragraph(f"<b>{i}.</b> {item}", body))
    story += [Spacer(1, 12), Paragraph("Representative thoughts", h2)] + [Paragraph(f'"{item}"', quote) for item in topic["quotes"]]
    story += [PageBreak(), Paragraph("Recommended validation plan", h2), Paragraph(topic["recommendation"], ParagraphStyle("Reco", parent=body, fontSize=13, leading=19, textColor=colors.HexColor("#1A1F30"))), Spacer(1, 18), Paragraph("Next study", h2), Paragraph("Run a focused concept test with real target users. Preserve the same segment definitions, test the leading objections directly, and compare observed behavior against stated pilot or purchase intent.", body), Spacer(1, 18), Paragraph("Methodology and limitations", h2), Paragraph("This report is generated from a hardcoded frontend demonstration containing nine curated personas and a deterministic thought timeline. It demonstrates the intended Snorkel product flow and report structure. It is not primary market research, a statistically representative survey, or evidence of actual customer demand.", body), Spacer(1, 35), Paragraph("Snorkel converts customer context into simulated reactions, comparable signals, and meeting-ready product decisions.", center)]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    copy2(path, PUBLIC / path.name)
    return path


if __name__ == "__main__":
    for item in TOPICS:
        print(build(item))
