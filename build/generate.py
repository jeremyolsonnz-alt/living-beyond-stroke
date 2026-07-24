#!/usr/bin/env python3
"""
generate.py — single source of truth -> audio scripts + PDFs + HTML partials.

Reads scripts/*.json (one per practice). Each paragraph is either:
  - a string (identical in all modes), or
  - an object {"agnostic","see","feel"} where the imagery cue differs by mode.

Outputs, per practice, into DIST:
  audio_scripts/<id>.txt         one narration script (agnostic; the inclusive
                                 version for recording — no "picture"/"watch"
                                 command that assumes a channel)
  pdf/<id>_both.pdf              printable script, standard wording (agnostic)
  pdf/<id>_see.pdf               printable script, wording for visualisers
  pdf/<id>_feel.pdf              printable script, wording for felt-sense
  partials/<id>_script.html      the HTML script block, agnostic as default,
                                 data-see / data-feel on paragraphs that vary
                                 (drop-in for the exercise page toggle)

Run:  python3 generate.py
"""
import json, os, glob, html

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "scripts")
DIST = "/mnt/user-data/outputs/stroke/dist"

MODES = ("both", "see", "feel")
MODE_KEY = {"both": "agnostic", "see": "see", "feel": "feel"}
MODE_LABEL = {
    "both": "Standard wording",
    "see":  "For people who picture things easily (visual)",
    "feel": "For people who feel movement rather than see it (kinesthetic)",
}

def para_text(p, mode):
    """Return the text of paragraph p in the requested mode."""
    if isinstance(p, str):
        return p
    return p.get(MODE_KEY[mode], p.get("agnostic"))

def varies(p):
    return isinstance(p, dict)

# ----------------------------------------------------------------- audio
def build_audio(practice):
    lines = []
    lines.append(practice["title"].upper())
    lines.append("Living Beyond Stroke — Guided Imagery Practice %s" % practice["number"])
    lines.append("Approx. %s. Narration script." % practice["duration"])
    lines.append("")
    lines.append("[ Read slowly. Allow 30–45 seconds per paragraph. Long pauses between phases. ]")
    lines.append("")
    for ph in practice["phases"]:
        lines.append("")
        lines.append("— %s —" % ph["label"].upper())
        lines.append("")
        for p in ph["paras"]:
            lines.append(para_text(p, "both"))   # agnostic narration
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"

# ----------------------------------------------------------------- pdf
def build_pdf(practice, mode, path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    HRFlowable, KeepTogether)
    from reportlab.lib.styles import ParagraphStyle

    CREAM = colors.HexColor("#F5F0E8")
    CHAR  = colors.HexColor("#2A2820")
    GOLD  = colors.HexColor("#C8963C")
    BODY  = colors.HexColor("#3A3428")
    MUTE  = colors.HexColor("#7A7060")

    styles = {
        "brand": ParagraphStyle("brand", fontName="Helvetica", fontSize=8,
                                textColor=GOLD, spaceAfter=2, leading=11,
                                tracking=1),
        "h1": ParagraphStyle("h1", fontName="Times-Roman", fontSize=22,
                             textColor=CHAR, spaceAfter=4, leading=26),
        "meta": ParagraphStyle("meta", fontName="Helvetica", fontSize=9,
                              textColor=MUTE, spaceAfter=2, leading=13),
        "mode": ParagraphStyle("mode", fontName="Helvetica-Oblique", fontSize=9,
                              textColor=GOLD, spaceBefore=6, spaceAfter=2, leading=13),
        "phase": ParagraphStyle("phase", fontName="Helvetica-Bold", fontSize=9,
                               textColor=GOLD, spaceBefore=16, spaceAfter=7,
                               leading=13),
        "body": ParagraphStyle("body", fontName="Times-Roman", fontSize=11.5,
                              textColor=BODY, spaceAfter=10, leading=18),
        "foot": ParagraphStyle("foot", fontName="Helvetica", fontSize=7.5,
                              textColor=MUTE, leading=11, spaceBefore=2),
    }

    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=20*mm, bottomMargin=18*mm,
                            leftMargin=22*mm, rightMargin=22*mm,
                            title="%s — Guided Imagery Script" % practice["title"],
                            author="Living Beyond Stroke")
    story = []
    story.append(Paragraph("LIVING BEYOND STROKE &nbsp;·&nbsp; GUIDED IMAGERY PRACTICE %s" % practice["number"], styles["brand"]))
    story.append(Paragraph(html.escape(practice["title"]), styles["h1"]))
    story.append(Paragraph("%s &nbsp;·&nbsp; %s" % (html.escape(practice["evidence"]), html.escape(practice["duration"])), styles["meta"]))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceAfter=6))
    story.append(Paragraph("This version: %s" % MODE_LABEL[mode], styles["mode"]))
    story.append(Paragraph("Read slowly — about 30–45 seconds per paragraph. There is no hurry.", styles["meta"]))

    for ph in practice["phases"]:
        block = [Paragraph(html.escape(ph["label"]).upper(), styles["phase"])]
        for p in ph["paras"]:
            txt = html.escape(para_text(p, mode))
            block.append(Paragraph(txt, styles["body"]))
        # keep each phase heading with at least its first paragraph
        story.append(KeepTogether(block[:2]))
        for flow in block[2:]:
            story.append(flow)

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.4, color=CREAM, spaceAfter=4))
    story.append(Paragraph(
        "Pathway: %s" % html.escape(practice["pathway_note"]), styles["foot"]))
    story.append(Paragraph(
        "Free educational resource. Not a medical service. Always work with your clinical team. "
        "The three-phase structure is the author's synthesis, not a clinically tested protocol as a unit.",
        styles["foot"]))
    doc.build(story)

# ----------------------------------------------------------------- html partial
def build_partial(practice):
    PHASE_STYLE = ("font-family:'Lora',serif;font-size:0.75rem;letter-spacing:0.1em;"
                   "text-transform:uppercase;color:var(--muted);margin-bottom:1.25rem;")
    out = []
    out.append("<!-- GENERATED from scripts/%s.json — do not edit by hand; edit the JSON and re-run generate.py -->" % practice["id"])
    nph = len(practice["phases"])
    for pi, ph in enumerate(practice["phases"]):
        out.append('<p style="%s">%s</p>' % (PHASE_STYLE, html.escape(ph["label"])))
        npar = len(ph["paras"])
        for idx, p in enumerate(ph["paras"]):
            last = (pi == nph-1) and (idx == npar-1)
            mb = "0" if last else ("1.75rem" if idx == npar-1 else "1rem")
            style = "margin-bottom:%s;" % mb
            agn = html.escape(para_text(p, "both"))
            if varies(p):
                see = html.escape(p["see"]).replace('"', "&quot;")
                feel = html.escape(p["feel"]).replace('"', "&quot;")
                out.append('<p style="%s" data-see="%s" data-feel="%s">%s</p>' % (style, see, feel, agn))
            else:
                out.append('<p style="%s">%s</p>' % (style, agn))
    return "\n".join(out) + "\n"

# ----------------------------------------------------------------- run
def main():
    os.makedirs(os.path.join(DIST, "audio_scripts"), exist_ok=True)
    os.makedirs(os.path.join(DIST, "pdf"), exist_ok=True)
    os.makedirs(os.path.join(DIST, "partials"), exist_ok=True)

    files = sorted(glob.glob(os.path.join(SRC, "*.json")))
    order = ["arm_hand","walking","balance","speech","fatigue"]
    files = sorted(files, key=lambda f: order.index(os.path.splitext(os.path.basename(f))[0]) if os.path.splitext(os.path.basename(f))[0] in order else 99)

    counts = {"audio":0,"pdf":0,"partial":0}
    for f in files:
        practice = json.load(open(f, encoding="utf-8"))
        pid = practice["id"]

        with open(os.path.join(DIST,"audio_scripts","%s.txt"%pid),"w",encoding="utf-8") as fh:
            fh.write(build_audio(practice)); counts["audio"] += 1

        for mode in MODES:
            build_pdf(practice, mode, os.path.join(DIST,"pdf","%s_%s.pdf"%(pid,mode)))
            counts["pdf"] += 1

        with open(os.path.join(DIST,"partials","%s_script.html"%pid),"w",encoding="utf-8") as fh:
            fh.write(build_partial(practice)); counts["partial"] += 1

        print("  built %-10s  audio + 3 PDFs + partial" % pid)

    print("\nTotals: %d audio scripts, %d PDFs, %d HTML partials" %
          (counts["audio"], counts["pdf"], counts["partial"]))

if __name__ == "__main__":
    main()
