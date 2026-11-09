#!/usr/bin/env python3
"""Builds dynamic, animated SVG assets for Guruvesh Bachhav's GitHub profile.
Features:
1. banner.svg: Animated hero with cycling typewriter subtitles + orbiting celestial system
2. solar-system.svg: Language planetary solar system with counter-rotating labels & satellites
3. pipeline.svg: Animated data flow with moving packets (React UI -> Python API -> Database -> AI/ML)
4. dsa-engine.svg: Animated progress bars + rotating scanner radar
5. terminal-journey.svg: Interactive Unix terminal with typewriter git-log
6. marquee.svg: Dual-direction infinite sliding skill ticker tape
7. status-badge.svg: Pulsing radar dispatch beacon
8. divider.svg: Subtle animated particle divider
"""

import os
import random
import xml.etree.ElementTree as ET

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def verify_and_save(filename, svg_str):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_str.strip())
    try:
        ET.parse(path)
        print(f"[OK] {filename}")
    except ET.ParseError as e:
        print(f"[ERROR] {filename}: {e}")
        raise e


# =====================================================================
# 1. ANIMATED HERO BANNER (960 x 280)
# =====================================================================
def make_banner():
    w, h = 960, 280
    random.seed(42)

    # Generate starry particle field
    stars = []
    for _ in range(65):
        sx = random.randint(15, w - 15)
        sy = random.randint(15, h - 15)
        sr = random.choice([0.6, 0.8, 1.1, 1.4])
        dur = round(random.uniform(2.0, 4.5), 1)
        delay = round(random.uniform(-4.0, 0), 1)
        stars.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#FFFFFF" opacity="0.6">'
                     f'<animate attributeName="opacity" values="0.1;0.95;0.1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle>')

    # Orbital solar center at (760, 140)
    cx, cy = 760, 140
    orbits = [
        (48, 9, "#E06D3B", "Py", 7, "#78A882", "ML"),      # Python + ML satellite
        (76, 14, "#F59E0B", "Java", 0, "", ""),            # Java
        (104, 20, "#60A5FA", "React", 0, "", ""),          # React
        (130, 28, "#34D399", "SQL", 0, "", ""),            # SQL/PostgreSQL
        (152, 38, "#A78BFA", "JS", 0, "", ""),             # JS
    ]

    orbit_rings = []
    orbiting_planets = []
    for r, dur, col, label, moon_r, moon_col, moon_lbl in orbits:
        orbit_rings.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#334155" stroke-opacity="0.4" stroke-dasharray="3 5"/>')
        
        moon_svg = ""
        if moon_r > 0:
            moon_svg = (f'<g><animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="3.5s" repeatCount="indefinite"/>'
                        f'<circle cx="{moon_r + 14}" r="5" fill="{moon_col}" stroke="#0F172A" stroke-width="1"/>'
                        f'<text x="{moon_r + 14}" y="2.5" text-anchor="middle" font-size="5" font-weight="700" fill="#0F172A" font-family="{SANS}">{moon_lbl}</text></g>')

        orbiting_planets.append(f'''
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>
      <g transform="translate({cx + r}, {cy})">
        <!-- Counter-rotate so text stays upright -->
        <g><animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="{dur}s" repeatCount="indefinite"/>
          <circle r="12" fill="{col}" stroke="#FFFFFF" stroke-opacity="0.3" stroke-width="1.5"/>
          <text y="3.5" text-anchor="middle" font-size="7.5" font-weight="700" fill="#0F172A" font-family="{SANS}">{label}</text>
          {moon_svg}
        </g>
      </g>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <defs>
    <linearGradient id="banner-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#090D16"/>
      <stop offset="50%" stop-color="#0E1322"/>
      <stop offset="100%" stop-color="#141B2D"/>
    </linearGradient>
    <radialGradient id="sun-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FBBF24" stop-opacity="0.6"/>
      <stop offset="60%" stop-color="#E06D3B" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#E06D3B" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="sun-core" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FEF3C7"/>
      <stop offset="50%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </radialGradient>
    <clipPath id="banner-clip"><rect width="{w}" height="{h}" rx="14"/></clipPath>
  </defs>

  <g clip-path="url(#banner-clip)">
    <!-- Deep Space Canvas -->
    <rect width="{w}" height="{h}" fill="url(#banner-bg)"/>
    <rect width="{w}" height="{h}" fill="none" stroke="#1E293B" stroke-width="1.5" rx="14"/>

    <!-- Twinkling Stardust Field -->
    {''.join(stars)}

    <!-- Solar Orbit System (Right Side) -->
    {''.join(orbit_rings)}
    
    <!-- Central Pulsing Star -->
    <circle cx="{cx}" cy="{cy}" r="36" fill="url(#sun-glow)">
      <animate attributeName="r" values="32;42;32" dur="3.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{cx}" cy="{cy}" r="22" fill="url(#sun-core)"/>
    <text x="{cx}" y="{cy + 3.5}" text-anchor="middle" font-size="7.5" font-weight="800" fill="#78350F" font-family="{SANS}">CORE</text>

    <!-- Planetary Orbits -->
    {''.join(orbiting_planets)}

    <!-- Left Side: Editorial & Personal Identity -->
    <g transform="translate(50, 48)">
      <!-- Top Status Chip -->
      <g>
        <rect width="210" height="24" rx="12" fill="#1E293B" fill-opacity="0.8" stroke="#334155" stroke-width="1"/>
        <circle cx="12" cy="12" r="4" fill="#10B981">
          <animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.7;1;0.7" dur="2s" repeatCount="indefinite"/>
        </circle>
        <text x="24" y="15.5" font-family="{MONO}" font-size="9" font-weight="700" fill="#6EE7B7" letter-spacing="1">AVAILABLE FOR SDE ROLES</text>
      </g>

      <!-- Main Name Heading -->
      <text x="0" y="70" font-family="{SANS}" font-size="44" font-weight="800" fill="#F8FAFC" letter-spacing="1">Guruvesh Bachhav</text>

      <!-- Subtitle Accent Tagline -->
      <text x="0" y="100" font-family="{SANS}" font-size="14" font-weight="500" fill="#94A3B8">
        Computer Engineering Student · <tspan fill="#F59E0B" font-weight="600">Python Backend</tspan> · <tspan fill="#60A5FA" font-weight="600">REST APIs</tspan> · <tspan fill="#34D399" font-weight="600">Applied AI/ML</tspan>
      </text>

      <!-- Thin Accent Line -->
      <rect x="0" y="116" width="60" height="3" rx="1.5" fill="#E06D3B"/>

      <!-- Cycling Dynamic Typewriter Terminal Messages -->
      <g transform="translate(0, 150)">
        <text font-family="{MONO}" font-size="13" font-weight="600" fill="#E06D3B" opacity="0">
          <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.22;0.25;1" dur="14s" begin="0s" repeatCount="indefinite"/>
          &gt; python_backend: architecting clean REST APIs &amp; SQL schemas
        </text>
        <text font-family="{MONO}" font-size="13" font-weight="600" fill="#38BDF8" opacity="0">
          <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.22;0.25;1" dur="14s" begin="3.5s" repeatCount="indefinite"/>
          &gt; dsa_progress: ~120 algorithmic solutions verified in Java
        </text>
        <text font-family="{MONO}" font-size="13" font-weight="600" fill="#34D399" opacity="0">
          <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.22;0.25;1" dur="14s" begin="7s" repeatCount="indefinite"/>
          &gt; shipped_systems: Crop Predictor, OCR Summarizer, Scholar Mentor
        </text>
        <text font-family="{MONO}" font-size="13" font-weight="600" fill="#FBBF24" opacity="0">
          <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.22;0.25;1" dur="14s" begin="10.5s" repeatCount="indefinite"/>
          &gt; engineering_philosophy: "Understand how it works. Then optimize it."
        </text>
      </g>
    </g>
  </g>
</svg>'''
    verify_and_save("banner.svg", svg)


# =====================================================================
# 2. LANGUAGE SOLAR SYSTEM (960 x 480)
# =====================================================================
def make_solar_system():
    w, h = 960, 480
    cx, cy = 480, 240
    random.seed(137)

    stars = []
    for _ in range(80):
        sx = random.randint(10, w - 10)
        sy = random.randint(10, h - 10)
        sr = random.choice([0.6, 0.8, 1.2, 1.5])
        dur = round(random.uniform(2.0, 5.0), 1)
        delay = round(random.uniform(-4.0, 0), 1)
        stars.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="#FFFFFF" opacity="0.5">'
                     f'<animate attributeName="opacity" values="0.1;0.9;0.1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle>')

    # Planets orbiting the center
    planets = [
        # radius, period, color, label, moon_label, moon_col, desc
        (75, 12, "#FFD43B", "Python", "ML", "#A78BFA", "Backend, APIs, Scripts"),
        (120, 18, "#F89820", "Java", "DSA", "#38BDF8", "DSA & OOP Architecture"),
        (165, 26, "#61DAFB", "React", "", "", "Component UI State"),
        (205, 34, "#34D399", "Postgres", "SQL", "#10B981", "Relational Schemas"),
        (245, 44, "#F472B6", "JavaScript", "", "", "Modern Web Logic"),
        (280, 56, "#FB923C", "HTML/CSS", "", "", "Semantic Layouts"),
    ]

    rings_svg = []
    orbit_elements = []

    for r, dur, col, label, moon_lbl, moon_col, _ in planets:
        rings_svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#334155" stroke-opacity="0.35" stroke-dasharray="4 6"/>')

        moon_markup = ""
        if moon_lbl:
            moon_markup = (f'<g><animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="4s" repeatCount="indefinite"/>'
                           f'<circle cx="22" r="6.5" fill="{moon_col}" stroke="#0F172A" stroke-width="1.5"/>'
                           f'<text x="22" y="2.5" text-anchor="middle" font-size="5.5" font-weight="700" fill="#0F172A" font-family="{SANS}">{moon_lbl}</text></g>')

        orbit_elements.append(f'''
    <!-- Planet {label} -->
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>
      <g transform="translate({cx + r}, {cy})">
        <g><animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="{dur}s" repeatCount="indefinite"/>
          <circle r="16" fill="{col}" stroke="#FFFFFF" stroke-opacity="0.4" stroke-width="2"/>
          <text y="4" text-anchor="middle" font-size="8.5" font-weight="700" fill="#0F172A" font-family="{SANS}">{label}</text>
          {moon_markup}
        </g>
      </g>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <defs>
    <radialGradient id="solar-bg" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="60%" stop-color="#080C17"/>
      <stop offset="100%" stop-color="#030712"/>
    </radialGradient>
    <radialGradient id="center-sun" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FEF3C7"/>
      <stop offset="40%" stop-color="#FBBF24"/>
      <stop offset="100%" stop-color="#EA580C"/>
    </radialGradient>
    <radialGradient id="sun-halo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="solar-clip"><rect width="{w}" height="{h}" rx="16"/></clipPath>
  </defs>

  <g clip-path="url(#solar-clip)">
    <rect width="{w}" height="{h}" fill="url(#solar-bg)"/>
    <rect width="{w}" height="{h}" fill="none" stroke="#1E293B" stroke-width="1.5" rx="16"/>

    <!-- Ambient Stars -->
    {''.join(stars)}

    <!-- Orbit Tracks -->
    {''.join(rings_svg)}

    <!-- Center Sun Glow & Body -->
    <circle cx="{cx}" cy="{cy}" r="68" fill="url(#sun-halo)">
      <animate attributeName="r" values="58;74;58" dur="4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{cx}" cy="{cy}" r="40" fill="url(#center-sun)"/>
    <text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="11" font-weight="800" fill="#78350F" font-family="{SANS}">Guruvesh</text>

    <!-- Revolving Planets -->
    {''.join(orbit_elements)}

    <!-- Top Left Title Tag -->
    <g transform="translate(36, 36)">
      <text font-family="{MONO}" font-size="11" font-weight="700" fill="#F59E0B" letter-spacing="2">02 // TECHNICAL ECOSYSTEM &amp; ORBITS</text>
      <text y="20" font-family="{SANS}" font-size="13" fill="#94A3B8">Core technologies orbiting my active software stack · Moons represent active specializations</text>
    </g>

    <!-- Bottom Metric Footnote -->
    <text x="{w - 36}" y="{h - 24}" text-anchor="end" font-family="{MONO}" font-size="10" fill="#64748B" letter-spacing="1">
      ROTATION SPEED PROPORTIONAL TO REPOSITORY INTENSITY
    </text>
  </g>
</svg>'''
    verify_and_save("solar-system.svg", svg)


# =====================================================================
# 3. INTERACTIVE SYSTEM PIPELINE (960 x 300)
# =====================================================================
def make_pipeline():
    w, h = 960, 300
    cy = 140
    xs = [160, 480, 800]

    def make_node(nx, ny, title, sub, color, border_col):
        nw, nh = 190, 78
        return (f'<rect x="{nx - nw / 2}" y="{ny - nh / 2}" width="{nw}" height="{nh}" rx="10" fill="#0E1424" stroke="{border_col}" stroke-width="2"/>'
                f'<rect x="{nx - nw / 2}" y="{ny - nh / 2}" width="4" height="{nh}" rx="2" fill="{color}"/>'
                f'<text x="{nx}" y="{ny - 4}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{color}">{title}</text>'
                f'<text x="{nx}" y="{ny + 16}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#94A3B8">{sub}</text>')

    # Link paths
    p1 = f"M{xs[0] + 95} {cy - 16} H{xs[1] - 95}"   # Request 1 -> 2
    p2 = f"M{xs[1] - 95} {cy + 16} H{xs[0] + 95}"   # Response 2 -> 1
    p3 = f"M{xs[1] + 95} {cy - 16} H{xs[2] - 95}"   # Query 2 -> 3
    p4 = f"M{xs[2] - 95} {cy + 16} H{xs[1] + 95}"   # Rows 3 -> 2
    p5 = f"M{xs[1]} {cy + 39} V{cy + 85}"           # Ingestion to ML

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <defs>
    <linearGradient id="pipe-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#080C16"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <filter id="glow-p" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="{w}" height="{h}" rx="14" fill="url(#pipe-bg)" stroke="#1E293B" stroke-width="1.5"/>

  <!-- Top Title -->
  <text x="36" y="38" font-family="{MONO}" font-size="11" font-weight="700" fill="#38BDF8" letter-spacing="2">03 // ARCHITECTURAL DATAFLOW &amp; REQUEST LIFECYCLE</text>
  <text x="36" y="56" font-family="{SANS}" font-size="13" fill="#94A3B8">How client state, backend APIs, and storage pipelines interact in full-stack systems</text>

  <!-- Wire 1: HTTP Request -->
  <path d="{p1}" stroke="#38BDF8" stroke-opacity="0.3" stroke-width="2"/>
  <circle r="4.5" fill="#38BDF8" filter="url(#glow-p)">
    <animateMotion path="{p1}" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <text x="{(xs[0] + xs[1]) / 2}" y="{cy - 24}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="#38BDF8" font-weight="600">HTTP / JSON PAYLOAD</text>

  <!-- Wire 2: JSON Response -->
  <path d="{p2}" stroke="#F472B6" stroke-opacity="0.3" stroke-width="2"/>
  <circle r="4.5" fill="#F472B6" filter="url(#glow-p)">
    <animateMotion path="{p2}" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <text x="{(xs[0] + xs[1]) / 2}" y="{cy + 34}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="#F472B6" font-weight="600">RESPONSE STREAM</text>

  <!-- Wire 3: SQL Query -->
  <path d="{p3}" stroke="#34D399" stroke-opacity="0.3" stroke-width="2"/>
  <circle r="4.5" fill="#34D399" filter="url(#glow-p)">
    <animateMotion path="{p3}" dur="1.9s" repeatCount="indefinite"/>
  </circle>
  <text x="{(xs[1] + xs[2]) / 2}" y="{cy - 24}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="#34D399" font-weight="600">SQL QUERIES / POOL</text>

  <!-- Wire 4: Database Rows -->
  <path d="{p4}" stroke="#FBBF24" stroke-opacity="0.3" stroke-width="2"/>
  <circle r="4.5" fill="#FBBF24" filter="url(#glow-p)">
    <animateMotion path="{p4}" dur="2.1s" repeatCount="indefinite"/>
  </circle>
  <text x="{(xs[1] + xs[2]) / 2}" y="{cy + 34}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="#FBBF24" font-weight="600">ROWSETS &amp; RELATIONS</text>

  <!-- Branch Wire: ML Ingestion -->
  <path d="{p5}" stroke="#A78BFA" stroke-opacity="0.4" stroke-width="2" stroke-dasharray="4 4"/>
  <circle r="4" fill="#A78BFA" filter="url(#glow-p)">
    <animateMotion path="{p5}" dur="1.7s" repeatCount="indefinite"/>
  </circle>

  <!-- Nodes -->
  {make_node(xs[0], cy, "Client UI", "React · Modern JS · HTML/CSS", "#60A5FA", "#2563EB")}
  {make_node(xs[1], cy, "Python API", "FastAPI / Flask · REST · Auth", "#F59E0B", "#D97706")}
  {make_node(xs[2], cy, "Data Persistence", "PostgreSQL · MySQL · MongoDB", "#34D399", "#059669")}

  <!-- Bottom ML Engine Node -->
  <g transform="translate({xs[1] - 110}, {cy + 85})">
    <rect width="220" height="42" rx="8" fill="#17122B" stroke="#8B5CF6" stroke-width="1.5" stroke-dasharray="6 4"/>
    <text x="110" y="18" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="#C4B5FD">Applied AI/ML Engine</text>
    <text x="110" y="32" text-anchor="middle" font-family="{MONO}" font-size="8.5" fill="#A78BFA">Scikit-Learn · OCR Pipeline · Predictions</text>
  </g>
</svg>'''
    verify_and_save("pipeline.svg", svg)


# =====================================================================
# 4. ANIMATED DSA RADAR & TELEMETRY ENGINE (960 x 320)
# =====================================================================
def make_dsa_engine():
    w, h = 960, 320
    topics = [
        ("Arrays &amp; Vectors", 1.0, "DONE", "12 problems"),
        ("Strings &amp; Manipulation", 1.0, "DONE", "14 problems"),
        ("Patterns &amp; Logic", 1.0, "DONE", "16 problems"),
        ("Bit Manipulation", 1.0, "DONE", "10 problems"),
        ("2D Arrays &amp; Matrix", 1.0, "DONE", "12 problems"),
        ("Sorting Algorithms", 1.0, "DONE", "8 algorithms"),
        ("Recursion &amp; Backtracking", 0.50, "ACTIVE", "In Progress"),
    ]

    bars_svg = []
    T = 5.0
    for i, (name, frac, status, count_str) in enumerate(topics):
        y = 86 + i * 31
        track_w = 210
        fill_w = track_w * frac
        col = "#10B981" if frac == 1.0 else "#F59E0B"
        d0 = 0.3 + i * 0.2

        bars_svg.append(f'''
    <!-- Topic {name} -->
    <g transform="translate(36, {y})">
      <text x="0" y="12" font-family="{SANS}" font-size="12.5" font-weight="600" fill="#E2E8F0">{name}</text>
      
      <!-- Track -->
      <rect x="220" y="2" width="{track_w}" height="12" rx="6" fill="#1E293B"/>
      
      <!-- Animated Fill -->
      <rect x="220" y="2" width="{fill_w:.1f}" height="12" rx="6" fill="{col}">
        <animate attributeName="width" values="0;0;{fill_w:.1f}" keyTimes="0;{d0 / T:.3f};{(d0 + 1.2) / T:.3f}" dur="{T}s" fill="freeze"/>
      </rect>
      
      <!-- Status Tag -->
      <text x="445" y="12" font-family="{MONO}" font-size="9" font-weight="700" fill="{col}">{status}</text>
      <text x="500" y="12" font-family="{MONO}" font-size="8.5" fill="#64748B">({count_str})</text>
    </g>''')

    # Radar on Right side at (770, 160)
    rx, ry = 770, 165
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <defs>
    <linearGradient id="dsa-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B0F19"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="radar-sweep" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#10B981" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#10B981" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{w}" height="{h}" rx="14" fill="url(#dsa-bg)" stroke="#1E293B" stroke-width="1.5"/>

  <!-- Header -->
  <text x="36" y="38" font-family="{MONO}" font-size="11" font-weight="700" fill="#10B981" letter-spacing="2">05 // ALGORITHMIC DEPTH &amp; DSA TELEMETRY</text>
  <text x="36" y="56" font-family="{SANS}" font-size="13" fill="#94A3B8">Solved in Java · Repository: github.com/Guruvesh03/DSA-in-Java</text>

  <!-- Big Counter -->
  <g transform="translate({w - 36}, 42)">
    <text text-anchor="end" font-family="{SANS}" font-size="32" font-weight="800" fill="#F59E0B">~120</text>
    <text y="16" text-anchor="end" font-family="{MONO}" font-size="9.5" fill="#94A3B8">PROBLEMS SOLVED</text>
  </g>

  <!-- Progress Bars -->
  {''.join(bars_svg)}

  <!-- Vertical Divider -->
  <line x1="620" y1="75" x2="620" y2="{h - 25}" stroke="#1E293B" stroke-width="1"/>

  <!-- Radar Scope Display -->
  <g transform="translate({rx}, {ry})">
    <circle r="75" fill="#06121E" stroke="#1E293B" stroke-width="1"/>
    <circle r="52" fill="none" stroke="#1E3A5F" stroke-width="1" stroke-dasharray="3 3"/>
    <circle r="28" fill="none" stroke="#1E3A5F" stroke-width="1"/>
    <line x1="-75" y1="0" x2="75" y2="0" stroke="#1E3A5F" stroke-width="0.75"/>
    <line x1="0" y1="-75" x2="0" y2="75" stroke="#1E3A5F" stroke-width="0.75"/>

    <!-- Rotating Radar Scanner Sweep -->
    <path d="M 0 0 L 75 0 A 75 75 0 0 1 0 75 Z" fill="url(#radar-sweep)">
      <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="4s" repeatCount="indefinite"/>
    </path>

    <!-- Radar Blips -->
    <circle cx="28" cy="-35" r="3.5" fill="#10B981">
      <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="-38" cy="22" r="3.5" fill="#F59E0B">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="44" cy="24" r="3" fill="#60A5FA">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="3s" repeatCount="indefinite"/>
    </circle>

    <!-- Radar Center -->
    <circle r="3" fill="#10B981"/>
    <text y="92" text-anchor="middle" font-family="{MONO}" font-size="8.5" fill="#64748B" letter-spacing="1">JAVA ALG-RADAR SCAN</text>
  </g>
</svg>'''
    verify_and_save("dsa-engine.svg", svg)


# =====================================================================
# 5. ANIMATED TYPEWRITER TERMINAL JOURNEY (960 x 300)
# =====================================================================
def make_terminal_journey():
    w, h = 960, 300
    top = 42

    log_entries = [
        ("guruvesh@dev:~$ git log --graph --oneline -n 5", "#F8FAFC", True),
        ("* 2027      (next)   Graduate and step into full-time SDE / Backend engineering", "#F59E0B", False),
        ("* Nov 2026  (HEAD)   Architected profile systems, Java DSA problem solving ongoing", "#10B981", False),
        ("* Oct 2026           Specialized in Python backend, PostgreSQL schemas & REST APIs", "#60A5FA", False),
        ("* Jan-Feb 26 (intern) Data Science / AI-ML intern @ Supratech AI Solutions", "#C084FC", False),
        ("                      Shipped Crop Predictor, Summary Generator, Scholar Mentor", "#94A3B8", False),
        ("* Earlier            B.E. Computer Engineering @ SPPU (PVG's COE & SSDIOM, Nashik)", "#E2E8F0", False),
    ]

    lines_svg = []
    for i, (text_line, col, is_prompt) in enumerate(log_entries):
        ly = top + 34 + i * 26
        weight = "700" if is_prompt else "500"
        lines_svg.append(f'<text x="32" y="{ly}" font-family="{MONO}" font-size="12.5" font-weight="{weight}" fill="{col}">{esc(text_line)}</text>')

    # Blinking cursor after the last line
    cur_y = top + 34 + len(log_entries) * 26
    lines_svg.append(f'''
    <g transform="translate(32, {cur_y})">
      <text font-family="{MONO}" font-size="12.5" font-weight="700" fill="#10B981">guruvesh@dev:~$ </text>
      <rect x="145" y="-12" width="8" height="16" fill="#10B981">
        <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
      </rect>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <!-- Window Container -->
  <rect width="{w}" height="{h}" rx="12" fill="#0B0F19" stroke="#1E293B" stroke-width="1.5"/>

  <!-- Title Bar -->
  <path d="M 0 12 A 12 12 0 0 1 12 0 H {w - 12} A 12 12 0 0 1 {w} 12 V {top} H 0 Z" fill="#141C2E"/>
  <line x1="0" y1="{top}" x2="{w}" y2="{top}" stroke="#1E293B" stroke-width="1"/>

  <!-- macOS Window Controls -->
  <circle cx="26" cy="21" r="6" fill="#EF4444"/>
  <circle cx="46" cy="21" r="6" fill="#F59E0B"/>
  <circle cx="66" cy="21" r="6" fill="#10B981"/>

  <!-- Window Title -->
  <text x="{w / 2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="600" fill="#94A3B8">guruvesh@dev: ~/journey (zsh)</text>

  <!-- Terminal Content Lines -->
  {''.join(lines_svg)}
</svg>'''
    verify_and_save("terminal-journey.svg", svg)


# =====================================================================
# 6. DUAL-ROW INFINITE SKILL MARQUEE (960 x 170)
# =====================================================================
def make_marquee():
    w, h = 960, 170
    row1 = ["Python", "Java", "PostgreSQL", "REST APIs", "React", "SQL", "MongoDB", "Git", "Streamlit", "DSA in Java", "OOP"]
    row2 = ["System Design", "Computer Networks", "Document OCR", "Machine Learning", "Scikit-Learn", "Docker", "Linux Shell", "FastAPI"]

    colors1 = ["#38BDF8", "#F59E0B", "#10B981", "#60A5FA", "#F472B6", "#A78BFA"]
    colors2 = ["#34D399", "#FB923C", "#818CF8", "#F43F5E", "#38BDF8", "#A3E635"]

    def build_chips(items, palette, y):
        chips = []
        x = 0
        for i, item in enumerate(items):
            cw = len(item) * 8.5 + 44
            col = palette[i % len(palette)]
            chips.append(f'''
      <g transform="translate({x:.1f}, {y})">
        <rect width="{cw:.1f}" height="36" rx="18" fill="#111827" stroke="{col}" stroke-width="1.2"/>
        <circle cx="16" cy="18" r="3.5" fill="{col}"/>
        <text x="28" y="22.5" font-family="{SANS}" font-size="13" font-weight="600" fill="#F3F4F6">{item}</text>
      </g>''')
            x += cw + 14
        return "".join(chips), x

    chips1, total1 = build_chips(row1, colors1, 38)
    chips2, total2 = build_chips(row2, colors2, 94)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <defs>
    <linearGradient id="fade-edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="6%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="94%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>
    <mask id="edge-mask">
      <rect width="{w}" height="{h}" fill="url(#fade-edge)"/>
    </mask>
  </defs>

  <rect width="{w}" height="{h}" rx="14" fill="#0A0E1A" stroke="#1E293B" stroke-width="1.5"/>

  <!-- Top Annotation -->
  <text x="32" y="24" font-family="{MONO}" font-size="9" font-weight="700" fill="#F59E0B" letter-spacing="2">ACTIVE SKILLS &amp; ARCHITECTURAL STACK</text>

  <g mask="url(#edge-mask)">
    <!-- Row 1: Left to Right -->
    <g>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-{total1:.1f} 0" dur="24s" repeatCount="indefinite"/>
      {chips1}
      <g transform="translate({total1:.1f}, 0)">{chips1}</g>
    </g>

    <!-- Row 2: Right to Left -->
    <g>
      <animateTransform attributeName="transform" type="translate" from="-{total2:.1f} 0" to="0 0" dur="28s" repeatCount="indefinite"/>
      {chips2}
      <g transform="translate({total2:.1f}, 0)">{chips2}</g>
    </g>
  </g>
</svg>'''
    verify_and_save("marquee.svg", svg)


# =====================================================================
# 7. PULSING RADAR STATUS BADGE (960 x 54)
# =====================================================================
def make_status_badge():
    w, h = 960, 54
    per = 2 * (w - 6 - 44) + 2 * 3.1416 * 22

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <defs>
    <filter id="radar-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Capsule Border with Animated Luminous Tracer -->
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="25" fill="#0B101D" stroke="#1E293B" stroke-width="1.5"/>
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="25" fill="none" stroke="#10B981" stroke-width="2" stroke-dasharray="140 {per - 140:.0f}" filter="url(#radar-glow)">
    <animate attributeName="stroke-dashoffset" from="0" to="-{per:.0f}" dur="7s" repeatCount="indefinite"/>
  </rect>

  <!-- Pulsing Radar Beacon -->
  <circle cx="36" cy="27" r="7" fill="#10B981" filter="url(#radar-glow)">
    <animate attributeName="r" values="5;9;5" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  <circle cx="36" cy="27" r="3" fill="#FFFFFF"/>

  <!-- Status Text Items -->
  <text x="56" y="32" font-family="{MONO}" font-size="11" font-weight="800" fill="#10B981" letter-spacing="2">OPEN TO WORK</text>
  <text x="180" y="32" font-family="{MONO}" font-size="11" fill="#475569">│</text>
  <text x="200" y="32" font-family="{SANS}" font-size="13" font-weight="600" fill="#F8FAFC">Targeting SDE &amp; Python Backend Engineering Roles</text>
  <text x="600" y="32" font-family="{MONO}" font-size="11" fill="#475569">│</text>
  <text x="620" y="32" font-family="{SANS}" font-size="13" fill="#94A3B8">Pune · Bangalore · Remote</text>
  <text x="820" y="32" font-family="{MONO}" font-size="11" fill="#475569">│</text>
  <text x="{w - 28}" y="32" text-anchor="end" font-family="{MONO}" font-size="11" font-weight="700" fill="#F59E0B">CLASS OF 2027</text>
</svg>'''
    verify_and_save("status-badge.svg", svg)


# =====================================================================
# 8. SUBTLE DIVIDER (960 x 32)
# =====================================================================
def make_divider():
    w, h = 960, 32
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <line x1="40" y1="16" x2="{w / 2 - 30}" y2="16" stroke="#334155" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="{w / 2 + 30}" y1="16" x2="{w - 40}" y2="16" stroke="#334155" stroke-width="1" stroke-dasharray="3 3"/>
  <polygon points="{w / 2},10 {w / 2 + 6},16 {w / 2},22 {w / 2 - 6},16" fill="#E06D3B"/>
</svg>'''
    verify_and_save("divider.svg", svg)


# =====================================================================
# 9. FOOTER BADGE (960 x 90)
# =====================================================================
def make_footer():
    w, h = 960, 90
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" fill="none">
  <rect width="{w}" height="{h}" rx="12" fill="#090D16" stroke="#1E293B" stroke-width="1.5"/>
  <circle cx="48" cy="45" r="16" fill="#1E293B"/>
  <text x="48" y="50" text-anchor="middle" font-family="{SANS}" font-size="11" font-weight="800" fill="#E06D3B">GB</text>

  <text x="80" y="40" font-family="{SANS}" font-size="13" font-weight="700" fill="#F8FAFC">Designed with intention · Built with pure animated vector SVG</text>
  <text x="80" y="58" font-family="{MONO}" font-size="10" fill="#64748B">© 2026 Guruvesh Bachhav · Savitribai Phule Pune University (SPPU)</text>

  <text x="{w - 36}" y="49" text-anchor="end" font-family="{MONO}" font-size="10" font-weight="700" fill="#10B981">
    ALL SYSTEMS OPERATIONAL ●
  </text>
</svg>'''
    verify_and_save("footer.svg", svg)


if __name__ == "__main__":
    make_banner()
    make_solar_system()
    make_pipeline()
    make_dsa_engine()
    make_terminal_journey()
    make_marquee()
    make_status_badge()
    make_divider()
    make_footer()
    print("All animated assets generated and XML-verified successfully!")
