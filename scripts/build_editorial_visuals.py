#!/usr/bin/env python3
"""Builds pristine, GitHub-compliant Swiss Editorial SVG assets for Guruvesh Bachhav.
- 100% pure SVG (no foreignObject, 100% Camo proxy safe)
- Valid XML with strict escaping
- Pixel-perfect typography & spacing
- Dark and Light mode variants
"""

import os
import xml.etree.ElementTree as ET

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# PALETTE DEFINITIONS (Swiss Editorial & Technical Notebook)
# ---------------------------------------------------------
DARK = {
    "bg": "#0E1013",
    "card_bg": "#15171C",
    "card_subtle": "#111317",
    "border": "#23262E",
    "border_subtle": "#1A1D24",
    "accent": "#E06D3B",            # Terracotta / Burnt Orange
    "accent_dim": "#C45B2C",
    "accent_bg": "rgba(224, 109, 59, 0.12)",
    "text_primary": "#F4F0EA",      # Warm Ivory
    "text_secondary": "#A2A7B4",    # Readable Muted Slate
    "text_muted": "#757B8A",        # Readable Technical Grey
    "text_subtle": "#4B515F",
    "success": "#78A882",           # Muted Olive Sage
    "grid_line": "#181A20",
}

LIGHT = {
    "bg": "#F9F7F3",
    "card_bg": "#FFFFFF",
    "card_subtle": "#F3EFE9",
    "border": "#E2DDD3",
    "border_subtle": "#EDE8DE",
    "accent": "#C65324",            # Deep Burnt Orange
    "accent_dim": "#A8441B",
    "accent_bg": "rgba(198, 83, 36, 0.08)",
    "text_primary": "#15171A",      # Deep Charcoal
    "text_secondary": "#4E5460",    # Readable Warm Charcoal
    "text_muted": "#767D8C",        # Readable Technical Stone
    "text_subtle": "#BAC0CC",
    "success": "#527E5A",           # Olive
    "grid_line": "#F0EBE1",
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SF Mono', Consolas, 'IBM Plex Mono', 'Courier New', monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def save_and_verify(filename, svg_code):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_code.strip())
    try:
        ET.parse(path)
        print(f"[OK] {filename}")
    except ET.ParseError as e:
        print(f"[ERROR] {filename}: {e}")
        raise e


# =====================================================================
# 1. EDITORIAL HEADER (310px)
# =====================================================================
def make_header(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 310

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <defs>
    <pattern id="grid-header-{theme}" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{c['grid_line']}" stroke-width="0.75"/>
    </pattern>
  </defs>

  <!-- Background Canvas -->
  <rect width="{w}" height="{h}" fill="{c['bg']}"/>
  <rect width="{w}" height="{h}" fill="url(#grid-header-{theme})"/>

  <!-- Outer Framing -->
  <rect x="16" y="16" width="{w - 32}" height="{h - 32}" fill="none" stroke="{c['border']}" stroke-width="1"/>

  <!-- Corner Crosshairs -->
  <path d="M 10 16 H 22 M 16 10 V 22" stroke="{c['accent']}" stroke-width="1.2"/>
  <path d="M {w - 22} 16 H {w - 10} M {w - 16} 10 V 22" stroke="{c['accent']}" stroke-width="1.2"/>
  <path d="M 10 {h - 16} H 22 M 16 {h - 22} V {h - 10}" stroke="{c['accent']}" stroke-width="1.2"/>
  <path d="M {w - 22} {h - 16} H {w - 10} M {w - 16} {h - 22} V {h - 10}" stroke="{c['accent']}" stroke-width="1.2"/>

  <!-- Top Folio Bar -->
  <line x1="16" y1="52" x2="{w - 16}" y2="52" stroke="{c['border']}" stroke-width="1"/>
  <text x="36" y="38" font-family="{MONO}" font-size="9" fill="{c['accent']}" letter-spacing="2" font-weight="700">FOLIO // 2026–2027</text>
  <text x="210" y="38" font-family="{MONO}" font-size="9" fill="{c['text_muted']}" letter-spacing="1.5">SYS.ID: GB-03 / SPPU-CE</text>
  <text x="440" y="38" font-family="{MONO}" font-size="9" fill="{c['text_muted']}" letter-spacing="1.5">PUNE · BANGALORE</text>
  <text x="{w - 36}" y="38" font-family="{MONO}" font-size="9" fill="{c['success']}" letter-spacing="1.5" text-anchor="end">STATUS: OPEN TO WORK ↗</text>

  <!-- Section Index -->
  <text x="44" y="94" font-family="{MONO}" font-size="10" fill="{c['accent']}" letter-spacing="3" font-weight="700">00 / PERSONAL IDENTITY &amp; ARCHITECTURE</text>

  <!-- Name -->
  <text x="44" y="152" font-family="{SANS}" font-size="46" font-weight="800" fill="{c['text_primary']}" letter-spacing="5">GURUVESH BACHHAV</text>

  <!-- Accent Rule -->
  <line x1="44" y1="172" x2="160" y2="172" stroke="{c['accent']}" stroke-width="2.5"/>

  <!-- Disciplines -->
  <text x="44" y="206" font-family="{MONO}" font-size="13" font-weight="600" fill="{c['text_primary']}" letter-spacing="2">SOFTWARE DEVELOPMENT ENGINEER &amp; SYSTEMS BUILDER</text>
  <text x="44" y="232" font-family="{MONO}" font-size="11" fill="{c['text_secondary']}" letter-spacing="1">SPECIALIZATION: PYTHON BACKEND · REST APIS · DATA PIPELINES · APPLIED AI/ML</text>
  <text x="44" y="254" font-family="{MONO}" font-size="10" fill="{c['text_muted']}" letter-spacing="1">FOUNDATIONS: DATA STRUCTURES &amp; ALGORITHMS IN JAVA (~120 SOLVED) · SYSTEM DESIGN</text>

  <!-- Right Technical Dossier Box -->
  <g transform="translate({w - 240}, 84)">
    <rect x="0" y="0" width="196" height="176" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>
    <rect x="0" y="0" width="196" height="26" fill="{c['card_subtle']}"/>
    <text x="12" y="17" font-family="{MONO}" font-size="8.5" font-weight="700" fill="{c['accent']}" letter-spacing="1.5">TECHNICAL DOSSIER</text>
    
    <text x="12" y="48" font-family="{MONO}" font-size="8" fill="{c['text_muted']}" letter-spacing="1">DEGREE</text>
    <text x="12" y="62" font-family="{SANS}" font-size="10.5" font-weight="600" fill="{c['text_primary']}">B.E. Computer Eng.</text>
    <text x="12" y="74" font-family="{MONO}" font-size="8" fill="{c['text_muted']}">SPPU · Graduating 2027</text>

    <line x1="12" y1="86" x2="184" y2="86" stroke="{c['border']}" stroke-width="0.75"/>

    <text x="12" y="104" font-family="{MONO}" font-size="8" fill="{c['text_muted']}" letter-spacing="1">EXPERIENCE</text>
    <text x="12" y="118" font-family="{SANS}" font-size="10.5" font-weight="600" fill="{c['text_primary']}">AI/ML &amp; Data Intern</text>
    <text x="12" y="130" font-family="{MONO}" font-size="8" fill="{c['text_muted']}">Supratech AI Solutions</text>

    <line x1="12" y1="142" x2="184" y2="142" stroke="{c['border']}" stroke-width="0.75"/>

    <text x="12" y="160" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{c['accent']}">GB.ENGINEERING</text>
    <text x="184" y="160" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}" text-anchor="end">REV. 03</text>
  </g>

  <!-- Bottom Framing Bar -->
  <line x1="16" y1="{h - 38}" x2="{w - 16}" y2="{h - 38}" stroke="{c['border']}" stroke-width="1"/>
  <text x="36" y="{h - 24}" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}" letter-spacing="1.5">“FIRST UNDERSTAND HOW IT WORKS — THEN OPTIMIZE IT.”</text>
  <text x="{w - 36}" y="{h - 24}" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}" letter-spacing="1.5" text-anchor="end">PUNE · BANGALORE · INDIA</text>
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 2. STATUS RIBBON (46px)
# =====================================================================
def make_status(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 46

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <rect x="0" y="0" width="{w}" height="{h}" rx="4" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>
  <rect x="0" y="0" width="4" height="{h}" rx="2" fill="{c['accent']}"/>

  <!-- Pulsing Dot -->
  <circle cx="28" cy="23" r="5" fill="{c['accent']}"/>
  <circle cx="28" cy="23" r="8" fill="none" stroke="{c['accent']}" stroke-width="1" opacity="0.45"/>

  <text x="46" y="27" font-family="{MONO}" font-size="10" font-weight="700" fill="{c['accent']}" letter-spacing="2">ACTIVE DISPATCH</text>
  <text x="180" y="27" font-family="{MONO}" font-size="10" fill="{c['text_muted']}">│</text>

  <text x="200" y="27" font-family="{MONO}" font-size="10" font-weight="600" fill="{c['text_primary']}" letter-spacing="1.5">TARGETING SDE &amp; PYTHON BACKEND ROLES</text>
  <text x="560" y="27" font-family="{MONO}" font-size="10" fill="{c['text_muted']}">│</text>

  <text x="580" y="27" font-family="{MONO}" font-size="10" fill="{c['text_secondary']}" letter-spacing="1">PUNE · BANGALORE · HYBRID</text>
  <text x="790" y="27" font-family="{MONO}" font-size="10" fill="{c['text_muted']}">│</text>

  <text x="{w - 24}" y="27" font-family="{MONO}" font-size="10" font-weight="600" fill="{c['text_primary']}" letter-spacing="1" text-anchor="end">GRADUATING 2027</text>
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 3. ABOUT / MANIFESTO BLOCK (220px) - FIXED WRAPPING & MARGINS
# =====================================================================
def make_about(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 220

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>

  <!-- Left Editorial Column (Restrained width to prevent right-side overlap) -->
  <g transform="translate(36, 26)">
    <text x="0" y="10" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{c['accent']}" letter-spacing="2.5">01 // PHILOSOPHY &amp; OBJECTIVE</text>
    
    <text x="0" y="44" font-family="{SANS}" font-size="18.5" font-weight="700" fill="{c['text_primary']}">
      A builder focused on understanding systems before optimizing them.
    </text>

    <text x="0" y="78" font-family="{SANS}" font-size="12" fill="{c['text_secondary']}">
      <tspan x="0" dy="0">Computer Engineering undergraduate at Savitribai Phule Pune University (SPPU), graduating Class of 2027.</tspan>
      <tspan x="0" dy="21">I design and engineer backend architectures with Python, structuring robust REST APIs, SQL schemas, and data pipelines.</tspan>
      <tspan x="0" dy="21">My algorithmic foundation is built in Java, maintaining rigorous practice across ~120+ verified data structures &amp; algorithms.</tspan>
      <tspan x="0" dy="21">Currently targeting Software Development Engineer (SDE) and Python backend engineering opportunities in Pune and Bangalore.</tspan>
    </text>
  </g>

  <!-- Vertical Divider (At x=650) -->
  <line x1="650" y1="20" x2="650" y2="{h - 20}" stroke="{c['border']}" stroke-width="1" stroke-dasharray="4 4"/>

  <!-- Right Telemetry Metrics (At x=676) -->
  <g transform="translate(676, 26)">
    <text x="0" y="10" font-family="{MONO}" font-size="9" font-weight="700" fill="{c['text_muted']}" letter-spacing="2">KEY METRICS</text>

    <text x="0" y="42" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}">PRIMARY FOCUS</text>
    <text x="0" y="58" font-family="{MONO}" font-size="11" font-weight="600" fill="{c['text_primary']}">Python · APIs · PostgreSQL</text>

    <text x="0" y="90" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}">DSA BENCHMARK</text>
    <text x="0" y="106" font-family="{MONO}" font-size="11" font-weight="600" fill="{c['accent']}">~120 Problems in Java</text>

    <text x="0" y="138" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}">INTERNSHIP SHIPPED</text>
    <text x="0" y="154" font-family="{MONO}" font-size="11" font-weight="600" fill="{c['text_primary']}">3 ML &amp; OCR Systems</text>
  </g>
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 4. TECHNICAL MATRIX / TOOLKIT (310px)
# =====================================================================
def make_toolkit(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 310

    col_w = (w - 32 - 36) / 4
    y_card = 20
    card_h = 200

    cols = [
        {
            "num": "01",
            "title": "LANGUAGES",
            "subtitle": "Core Execution",
            "items": [
                ("Python", "Backend systems, APIs, scripts"),
                ("Java", "Data structures, OOP, algorithms"),
                ("JavaScript", "Modern UI &amp; web interactions"),
                ("SQL", "Relational querying &amp; schemas"),
            ]
        },
        {
            "num": "02",
            "title": "BACKEND &amp; DATA",
            "subtitle": "Architecture &amp; Persistence",
            "items": [
                ("PostgreSQL", "Relational design &amp; indexing"),
                ("RESTful APIs", "HTTP design, payloads, routing"),
                ("MySQL", "Schema queries &amp; transactions"),
                ("MongoDB", "Document-oriented storage"),
            ]
        },
        {
            "num": "03",
            "title": "WEB &amp; INTERFACE",
            "subtitle": "Client-Side Engineering",
            "items": [
                ("React", "Component lifecycle &amp; state"),
                ("Streamlit", "Rapid ML application frontends"),
                ("Modern CSS3", "Grid systems, flexbox, layouts"),
                ("Semantic HTML5", "Accessible web document trees"),
            ]
        },
        {
            "num": "04",
            "title": "TOOLCHAIN &amp; SPEC",
            "subtitle": "Engineering Practices",
            "items": [
                ("Git &amp; GitHub", "Branching, PRs, version control"),
                ("DSA Foundations", "~120 vetted solutions in Java"),
                ("OOP Architecture", "SOLID principles &amp; patterns"),
                ("System Design", "Scalability, caching, networks"),
            ]
        }
    ]

    svg_cols = []
    for i, col in enumerate(cols):
        cx = 16 + i * (col_w + 12)
        items_svg = []
        for j, (tech, desc) in enumerate(col["items"]):
            iy = 72 + j * 32
            items_svg.append(f'''
      <g transform="translate(14, {iy})">
        <text x="0" y="0" font-family="{SANS}" font-size="12" font-weight="600" fill="{c['text_primary']}">{tech}</text>
        <text x="0" y="14" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}">{desc}</text>
      </g>''')

        svg_cols.append(f'''
    <!-- Column {col['num']} -->
    <g transform="translate({cx}, {y_card})">
      <rect x="0" y="0" width="{col_w}" height="{card_h}" rx="4" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>
      <line x1="0" y1="44" x2="{col_w}" y2="44" stroke="{c['border']}" stroke-width="1"/>
      
      <text x="14" y="24" font-family="{MONO}" font-size="9" font-weight="700" fill="{c['accent']}" letter-spacing="1.5">{col['num']} // {col['title']}</text>
      <text x="14" y="36" font-family="{MONO}" font-size="8" fill="{c['text_muted']}">{col['subtitle']}</text>
      {''.join(items_svg)}
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <!-- 4 Columns -->
  {''.join(svg_cols)}

  <!-- Bottom Deep Dive Banner -->
  <g transform="translate(16, 236)">
    <rect x="0" y="0" width="{w - 32}" height="58" rx="4" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="58" rx="2" fill="{c['accent']}"/>
    
    <text x="20" y="24" font-family="{MONO}" font-size="9" font-weight="700" fill="{c['accent']}" letter-spacing="2">ACTIVE EXPEDITIONS &amp; SYSTEM STUDY</text>
    <text x="20" y="44" font-family="{MONO}" font-size="10.5" fill="{c['text_secondary']}">
      Deepening expertise in <tspan font-weight="700" fill="{c['text_primary']}">Distributed Backend Systems</tspan> · <tspan font-weight="700" fill="{c['text_primary']}">PostgreSQL Optimization</tspan> · <tspan font-weight="700" fill="{c['text_primary']}">Computer Networks &amp; OS</tspan> · <tspan font-weight="700" fill="{c['text_primary']}">Applied AI/ML Pipelines</tspan>
    </text>
  </g>
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 5. CURATED PROJECTS DOSSIER (380px)
# =====================================================================
def make_projects(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 380
    card_w = (w - 32 - 32) / 3
    card_h = 340
    y_card = 20

    projects = [
        {
            "id": "ARCHIVE // 01",
            "title": "Crop Predictor",
            "type": "AGRONOMIC AI RECOMMENDATION",
            "period": "AI/ML Internship 2026",
            "desc_lines": [
                "Intelligent agricultural recommendation system",
                "developed during industry data science internship.",
                "Evaluates complex soil chemistry (N, P, K), rainfall,",
                "and environmental metrics to accurately predict",
                "optimal crop varieties for maximum yield.",
            ],
            "stack": ["PYTHON", "STREAMLIT", "SCIKIT-LEARN", "PANDAS"],
            "status": "COMPLETED &amp; VERIFIED",
        },
        {
            "id": "ARCHIVE // 02",
            "title": "Summary Generator",
            "type": "DOCUMENT VISION &amp; SYNTHESIS",
            "period": "Document Pipeline",
            "desc_lines": [
                "Automated text extraction and synthesis engine.",
                "Integrates optical character recognition (OCR) to",
                "ingest printed documentation and generate",
                "concise extractive summaries for dense technical",
                "literature and report comprehension.",
            ],
            "stack": ["PYTHON", "TESSERACT OCR", "TEXT PIPELINE", "NLP"],
            "status": "COMPLETED &amp; VERIFIED",
        },
        {
            "id": "ARCHIVE // 03",
            "title": "Scholar Mentor",
            "type": "ACADEMIC ROUTING PLATFORM",
            "period": "Mentorship Architecture",
            "desc_lines": [
                "Student-centric mentorship and academic routing",
                "platform designed to connect junior engineering",
                "students with senior mentors. Features structured",
                "curriculum roadmaps, study milestone tracking,",
                "and modular guidance workflows.",
            ],
            "stack": ["PYTHON", "DATA MODELS", "REST ARCHITECTURE"],
            "status": "CORE SYSTEM BUILT",
        }
    ]

    cards_svg = []
    for i, p in enumerate(projects):
        cx = 16 + i * (card_w + 16)
        desc_tspans = "".join(f'<tspan x="16" dy="17">{line}</tspan>' for line in p["desc_lines"])

        stack_svg = []
        cur_x = 16
        cur_y = 260
        for tag in p["stack"]:
            tag_w = len(tag) * 6.8 + 14
            if cur_x + tag_w > card_w - 16:
                cur_x = 16
                cur_y += 24
            stack_svg.append(f'''
      <rect x="{cur_x}" y="{cur_y}" width="{tag_w:.1f}" height="18" rx="2" fill="{c['card_subtle']}" stroke="{c['border']}" stroke-width="0.75"/>
      <text x="{cur_x + tag_w / 2:.1f}" y="{cur_y + 12}" font-family="{MONO}" font-size="8" font-weight="600" fill="{c['text_secondary']}" text-anchor="middle">{tag}</text>''')
            cur_x += tag_w + 6

        cards_svg.append(f'''
    <!-- Project Card {p['id']} -->
    <g transform="translate({cx}, {y_card})">
      <rect x="0" y="0" width="{card_w}" height="{card_h}" rx="5" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>
      
      <!-- Top Bar -->
      <rect x="0" y="0" width="{card_w}" height="36" rx="5" fill="{c['card_subtle']}"/>
      <line x1="0" y1="36" x2="{card_w}" y2="36" stroke="{c['border']}" stroke-width="1"/>
      
      <text x="16" y="23" font-family="{MONO}" font-size="9" font-weight="700" fill="{c['accent']}" letter-spacing="1.5">{p['id']}</text>
      <text x="{card_w - 16}" y="23" font-family="{MONO}" font-size="8" fill="{c['text_muted']}" text-anchor="end">{p['period']}</text>

      <!-- Title & Classification -->
      <text x="16" y="70" font-family="{SANS}" font-size="19" font-weight="700" fill="{c['text_primary']}">{p['title']}</text>
      <line x1="16" y1="80" x2="60" y2="80" stroke="{c['accent']}" stroke-width="2"/>
      
      <text x="16" y="100" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{c['text_muted']}" letter-spacing="1">{p['type']}</text>

      <!-- Description Lines -->
      <text x="16" y="112" font-family="{SANS}" font-size="11.5" fill="{c['text_secondary']}">
        {desc_tspans}
      </text>

      <!-- Technology Stack Header -->
      <line x1="16" y1="230" x2="{card_w - 16}" y2="230" stroke="{c['border']}" stroke-width="0.75"/>
      <text x="16" y="248" font-family="{MONO}" font-size="8" font-weight="700" fill="{c['text_muted']}" letter-spacing="1.5">STACK &amp; ENVIRONMENT</text>
      
      {''.join(stack_svg)}

      <!-- Bottom Card Status Footer -->
      <line x1="0" y1="{card_h - 32}" x2="{card_w}" y2="{card_h - 32}" stroke="{c['border']}" stroke-width="1"/>
      <circle cx="20" cy="{card_h - 16}" r="3" fill="{c['success']}"/>
      <text x="30" y="{card_h - 13}" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{c['text_secondary']}">{p['status']}</text>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  {''.join(cards_svg)}
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 6. DSA TELEMETRY BENCHMARK (260px) - FIXED RIGHT COLUMN OFFSET
# =====================================================================
def make_dsa(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 260

    col1 = [
        ("01", "Arrays &amp; Vectors", 1.0, "COMPLETE", "12/12 problems"),
        ("02", "Strings &amp; Search", 1.0, "COMPLETE", "14/14 problems"),
        ("03", "Patterns &amp; Matrix", 1.0, "COMPLETE", "16/16 problems"),
        ("04", "Bit Manipulation", 1.0, "COMPLETE", "10/10 problems"),
    ]
    col2 = [
        ("05", "2D Arrays &amp; Traversal", 1.0, "COMPLETE", "12/12 problems"),
        ("06", "Sorting Algorithms", 1.0, "COMPLETE", "8/8 algorithms"),
        ("07", "Recursion &amp; Backtrack", 0.45, "IN PROGRESS", "Active study"),
        ("08", "Linked Lists &amp; Trees", 0.15, "NEXT IN QUEUE", "Planned queue"),
    ]

    def render_col(col_items, offset_x):
        lines = []
        for i, (idx, name_str, frac, status_str, count_str) in enumerate(col_items):
            cy = 76 + i * 38
            bar_w = 110
            prog_w = int(bar_w * frac)
            is_done = frac >= 0.99
            bar_color = c['accent'] if is_done else (c['accent_dim'] if frac > 0.2 else c['border_subtle'])
            status_color = c['accent'] if is_done else (c['text_primary'] if frac > 0.2 else c['text_muted'])
            
            lines.append(f'''
      <!-- Topic {idx} -->
      <g transform="translate({offset_x}, {cy})">
        <text x="0" y="10" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}">{idx}</text>
        <text x="24" y="10" font-family="{SANS}" font-size="12" font-weight="600" fill="{c['text_primary']}">{name_str}</text>
        
        <!-- Track Bar -->
        <rect x="195" y="3" width="{bar_w}" height="6" rx="3" fill="{c['card_subtle']}" stroke="{c['border']}" stroke-width="0.75"/>
        <rect x="195" y="3" width="{prog_w}" height="6" rx="3" fill="{bar_color}"/>
        
        <!-- Telemetry Details -->
        <text x="320" y="9" font-family="{MONO}" font-size="8.5" font-weight="700" fill="{status_color}" letter-spacing="1">{status_str}</text>
        <text x="400" y="9" font-family="{MONO}" font-size="8" fill="{c['text_muted']}">({count_str})</text>
      </g>''')
        return "".join(lines)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <!-- Container Frame -->
  <rect x="16" y="16" width="{w - 32}" height="{h - 32}" rx="6" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>

  <!-- Top Telemetry Header -->
  <rect x="16" y="16" width="{w - 32}" height="38" rx="6" fill="{c['card_subtle']}"/>
  <line x1="16" y1="54" x2="{w - 16}" y2="54" stroke="{c['border']}" stroke-width="1"/>

  <text x="36" y="38" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{c['accent']}" letter-spacing="2">05 // ALGORITHMIC TELEMETRY: JAVA DATA STRUCTURES</text>
  <text x="{w - 36}" y="38" font-family="{MONO}" font-size="9" fill="{c['text_muted']}" letter-spacing="1" text-anchor="end">REPOSITORY: GURUVESH03/DSA-IN-JAVA ↗</text>

  <!-- Left Column -->
  {render_col(col1, 36)}

  <!-- Vertical Divider (At center x=480) -->
  <line x1="480" y1="66" x2="480" y2="{h - 32}" stroke="{c['border']}" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Right Column (Shifted to x=505 for comfortable margin) -->
  {render_col(col2, 505)}

  <!-- Bottom Milestone Counter Footnote -->
  <line x1="16" y1="{h - 40}" x2="{w - 16}" y2="{h - 40}" stroke="{c['border']}" stroke-width="0.75"/>
  <text x="36" y="{h - 26}" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}" letter-spacing="1">VERIFIED BENCHMARK: ~120 PROBLEMS SOLVED IN JAVA</text>
  <text x="{w - 36}" y="{h - 26}" font-family="{MONO}" font-size="8.5" font-weight="600" fill="{c['accent']}" letter-spacing="1" text-anchor="end">CONTINUOUS DAILY REPOSITORY COMMITS</text>
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 7. CHRONOLOGY & JOURNEY (180px)
# =====================================================================
def make_timeline(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 180

    milestones = [
        ("01", "2023 – 2027", "B.E. Computer Eng.", "SPPU (PVG's COE &amp; SSDIOM)", False),
        ("02", "JAN – FEB 2026", "AI/ML &amp; Data Intern", "Supratech AI Solutions", False),
        ("03", "OCT 2026", "Python Backend Core", "APIs, PostgreSQL &amp; Systems", False),
        ("04", "NOV 2026", "Systems &amp; DSA Depth", "~120 Java DSA Solutions", False),
        ("05", "2027 TARGET", "Full-Time SDE", "Targeting Pune &amp; Bangalore", True),
    ]

    m_w = (w - 64) / len(milestones)
    nodes_svg = []
    y_line = 70

    for i, (num, period, title, desc, is_target) in enumerate(milestones):
        cx = 32 + i * m_w + m_w / 2
        circle_fill = c['accent'] if is_target else c['card_bg']
        circle_stroke = c['accent']
        circle_r = 6 if is_target else 5
        pulse = f'<circle cx="{cx}" cy="{y_line}" r="10" fill="none" stroke="{c["accent"]}" stroke-width="1" opacity="0.35"/>' if is_target else ""

        nodes_svg.append(f'''
    <!-- Milestone {num} -->
    <g>
      {pulse}
      <circle cx="{cx}" cy="{y_line}" r="{circle_r}" fill="{circle_fill}" stroke="{circle_stroke}" stroke-width="2"/>
      
      <text x="{cx}" y="42" font-family="{MONO}" font-size="8.5" font-weight="700" fill="{c['accent']}" text-anchor="middle" letter-spacing="1">{num} // {period}</text>
      
      <text x="{cx}" y="104" font-family="{SANS}" font-size="12" font-weight="700" fill="{c['text_primary']}" text-anchor="middle">{title}</text>
      <text x="{cx}" y="122" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}" text-anchor="middle">{desc}</text>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>

  <text x="36" y="24" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{c['accent']}" letter-spacing="2">04 // CHRONOLOGY &amp; ENGINEERING PROGRESSION</text>

  <line x1="60" y1="{y_line}" x2="{w - 60}" y2="{y_line}" stroke="{c['border']}" stroke-width="1.5"/>

  {''.join(nodes_svg)}

  <line x1="36" y1="{h - 26}" x2="{w - 36}" y2="{h - 26}" stroke="{c['border']}" stroke-width="0.75"/>
  <text x="36" y="{h - 12}" font-family="{MONO}" font-size="8" fill="{c['text_muted']}" letter-spacing="1.5">EVOLUTION: ACADEMIC FOUNDATIONS → PRODUCTION DATA SCIENCE → SCALABLE BACKEND SYSTEMS</text>
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 8. GITHUB TELEMETRY & REPOSITORY ARCHIVE (220px)
# =====================================================================
def make_telemetry(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 220

    tiles = [
        ("PUBLIC REPOSITORIES", "13", "ACTIVE PROJECTS", "Python &amp; Java Core"),
        ("ALGORITHMIC PROBLEMS", "~120+", "VERIFIED SOLUTIONS", "Java DSA Archive"),
        ("ACADEMIC MILESTONE", "2027", "GRADUATION TARGET", "B.E. Computer Eng. (SPPU)"),
        ("ENGINEERING FOCUS", "SDE", "SYSTEMS &amp; BACKEND", "Pune · Bangalore Targets"),
    ]

    t_w = (w - 32 - 36) / 4
    tiles_svg = []
    for i, (label, val, sub, note) in enumerate(tiles):
        tx = 16 + i * (t_w + 12)
        tiles_svg.append(f'''
    <!-- Metric Tile {i + 1} -->
    <g transform="translate({tx}, 68)">
      <rect x="0" y="0" width="{t_w}" height="120" rx="4" fill="{c['card_subtle']}" stroke="{c['border']}" stroke-width="1"/>
      <rect x="0" y="0" width="3" height="120" rx="1.5" fill="{c['accent']}"/>
      
      <text x="14" y="22" font-family="{MONO}" font-size="8" font-weight="700" fill="{c['text_muted']}" letter-spacing="1">{label}</text>
      <text x="14" y="58" font-family="{SANS}" font-size="28" font-weight="800" fill="{c['text_primary']}">{val}</text>
      
      <line x1="14" y1="72" x2="{t_w - 14}" y2="72" stroke="{c['border']}" stroke-width="0.75"/>
      <text x="14" y="90" font-family="{MONO}" font-size="8.5" font-weight="700" fill="{c['accent']}">{sub}</text>
      <text x="14" y="104" font-family="{MONO}" font-size="8" fill="{c['text_muted']}">{note}</text>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <rect x="16" y="16" width="{w - 32}" height="{h - 32}" rx="6" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>
  
  <!-- Header Bar -->
  <rect x="16" y="16" width="{w - 32}" height="38" rx="6" fill="{c['card_subtle']}"/>
  <line x1="16" y1="54" x2="{w - 16}" y2="54" stroke="{c['border']}" stroke-width="1"/>
  
  <text x="36" y="38" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{c['accent']}" letter-spacing="2">06 // ENGINEERING TELEMETRY &amp; REPOSITORY BENCHMARK</text>
  <text x="{w - 36}" y="38" font-family="{MONO}" font-size="9" fill="{c['text_muted']}" letter-spacing="1" text-anchor="end">PROFILE: GITHUB.COM/GURUVESH03 ↗</text>

  {''.join(tiles_svg)}
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 9. EDITORIAL DIVIDERS (28px)
# =====================================================================
def make_divider(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 28

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <line x1="16" y1="14" x2="{w / 2 - 24}" y2="14" stroke="{c['border']}" stroke-width="0.75"/>
  <line x1="{w / 2 + 24}" y1="14" x2="{w - 16}" y2="14" stroke="{c['border']}" stroke-width="0.75"/>
  <rect x="{w / 2 - 4}" y="10" width="8" height="8" rx="1" fill="{c['accent']}" transform="rotate(45, {w / 2}, 14)"/>
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# 10. EDITORIAL COLOPHON / FOOTER (96px)
# =====================================================================
def make_footer(theme, name):
    c = DARK if theme == "dark" else LIGHT
    w, h = 960, 96

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <line x1="16" y1="1" x2="{w - 16}" y2="1" stroke="{c['border']}" stroke-width="1"/>

  <path d="M 12 1 H 20 M 16 -3 V 5" stroke="{c['accent']}" stroke-width="1"/>
  <path d="M {w - 20} 1 H {w - 12} M {w - 16} -3 V 5" stroke="{c['accent']}" stroke-width="1"/>

  <text x="36" y="36" font-family="{MONO}" font-size="9" font-weight="700" fill="{c['accent']}" letter-spacing="2">COLOPHON &amp; VERIFICATION</text>
  <text x="36" y="54" font-family="{MONO}" font-size="8.5" fill="{c['text_muted']}" letter-spacing="1">TYPESET IN EDITORIAL GROTESK &amp; JETBRAINS MONO · ARCHITECTURAL SWISS GRID SPECIFICATION</text>
  <text x="36" y="70" font-family="{MONO}" font-size="8" fill="{c['text_muted']}">DEVELOPED FOR GURUVESH BACHHAV · HOSTED ON GITHUB · CONTINUOUS INTEGRATION REFRESHED</text>

  <g transform="translate({w - 160}, 24)">
    <rect x="0" y="0" width="124" height="48" rx="3" fill="{c['card_bg']}" stroke="{c['border']}" stroke-width="1"/>
    <rect x="0" y="0" width="3" height="48" rx="1.5" fill="{c['accent']}"/>
    
    <text x="14" y="20" font-family="{MONO}" font-size="8" font-weight="700" fill="{c['accent']}">GURUVESH BACHHAV</text>
    <text x="14" y="36" font-family="{MONO}" font-size="7.5" fill="{c['text_muted']}">© 2026 · ALL RIGHTS RESERVED</text>
  </g>
</svg>'''
    save_and_verify(name, svg)


# =====================================================================
# MAIN RUNNER
# =====================================================================
if __name__ == "__main__":
    for theme in ["dark", "light"]:
        suffix = f"-{theme}.svg"
        make_header(theme, f"header{suffix}")
        make_status(theme, f"status{suffix}")
        make_about(theme, f"about{suffix}")
        make_toolkit(theme, f"toolkit{suffix}")
        make_projects(theme, f"projects{suffix}")
        make_dsa(theme, f"dsa{suffix}")
        make_timeline(theme, f"timeline{suffix}")
        make_telemetry(theme, f"telemetry{suffix}")
        make_divider(theme, f"divider{suffix}")
        make_footer(theme, f"footer{suffix}")

    print("All editorial visual assets generated and XML-verified successfully!")
