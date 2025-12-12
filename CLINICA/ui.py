# ui.py
import streamlit as st

# Paleta y tamaño
PRIMARY_BG = "#FAFAF8"
ACCENT = "#FFCC33"   # color queso
ACCENT_DARK = "#E6B800"
TEXT = "#1F2937"

CHEESE_SVG = """
<svg width="56" height="56" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Quesito">
  <title>Quesito</title>
  <!-- Triángulo base -->
  <polygon points="32,4 60,56 4,56" fill="#FFCC33" stroke="#E6B800" stroke-width="2"/>
  <!-- Huecos -->
  <circle cx="42" cy="28" r="4" fill="#F9E6A0"/>
  <circle cx="28" cy="36" r="3.2" fill="#F9E6A0"/>
  <circle cx="22" cy="22" r="2.8" fill="#F9E6A0"/>
  <!-- Sombra -->
  <path d="M4 56 L60 56 L32 4 Z" fill-opacity="0.02"/>
</svg>
"""

HERO_SVG = """
<svg viewBox="0 0 900 260" width="100%" height="180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mascotas">
  <defs>
    <linearGradient id="g1" x1="0" x2="1">
      <stop offset="0" stop-color="#fef3d9"/>
      <stop offset="1" stop-color="#fff7e6"/>
    </linearGradient>
  </defs>

  <!-- Fondo -->
  <rect x="0" y="0" width="900" height="260" fill="url(#g1)"/>

  <!-- Siluetas al fondo -->
  <g transform="translate(20,60)" fill="#D1D5DB" opacity="0.6">
    <!-- perro simple -->
    <path d="M60 70 q20 -40 60 -30 q20 5 40 0 q10 -3 20 10 q-10 8 -2 20 q-30 10 -70 10 q-20 0 -48 -10z"/>
    <!-- gato simple -->
    <path d="M220 80 q10 -30 40 -30 q12 0 20 6 q-8 10 -4 24 q-20 10 -56 10 q-8 0 -12 -10z" transform="translate(0,-6)"/>
    <!-- conejo -->
    <path d="M360 60 q8 -22 26 -18 q8 2 8 10 q-12 8 -8 22 q-18 8 -34 4 q-6 -4 -12 -18z" transform="translate(0,10)"/>
    <!-- ave -->
    <ellipse cx="480" cy="70" rx="26" ry="12"/>
    <!-- hámster/pez stylized -->
    <circle cx="580" cy="72" r="16"/>
  </g>

  <!-- Perro feliz en primer plano -->
  <g transform="translate(120,50)">
    <ellipse cx="420" cy="120" rx="120" ry="90" fill="#fff" opacity="0.35"/>
    <path d="M150 130 q30 -70 120 -70 q80 0 120 70 q-40 20 -160 20 q-120 0 -120 -20z" fill="#FFEDD5"/>
    <!-- cabeza -->
    <circle cx="300" cy="80" r="42" fill="#FFD28A"/>
    <ellipse cx="284" cy="90" rx="8" ry="12" fill="#4B5563"/>
    <ellipse cx="316" cy="90" rx="8" ry="12" fill="#4B5563"/>
    <path d="M286 100 q14 14 28 0" stroke="#4B5563" stroke-width="4" fill="none" stroke-linecap="round"/>
    <!-- oreja -->
    <path d="M264 62 q-20 20 -8 36 q18 -6 20 -24 z" fill="#E6A64F"/>
    <path d="M336 62 q20 20 8 36 q-18 -6 -20 -24 z" fill="#E6A64F"/>
  </g>

  <!-- Texto decorativo -->
  <text x="28" y="40" font-family="sans-serif" font-size="28" fill="#374151" font-weight="600">Clínica Quesitos</text>
  <text x="28" y="68" font-family="sans-serif" font-size="14" fill="#6B7280">Cerca de ti — Cuidado con cariño</text>
</svg>
"""

HEADER_CSS = f"""
<style>
/* Body background */
.stApp {{
  background-color: {PRIMARY_BG};
  color: {TEXT};
}}

/* Header fixed top-left */
.header-left {{
  position: fixed;
  top: 12px;
  left: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 9999;
  background: rgba(255,255,255,0.85);
  padding: 6px 10px;
  border-radius: 8px;
  box-shadow: 0 4px 14px rgba(16,24,40,0.06);
}}

.header-title {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  font-size: 15px;
  font-weight: 700;
  color: {TEXT};
  line-height: 1;
}}

.header-sub {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  font-size: 11px;
  color: #6B7280;
  margin-top: -2px;
}}

/* Main container padding so the header doesn't overlap content */
.main-with-header {{
  padding-top: 72px;
}}

/* Form box appearance for login/register */
.form-box {{
  background: white;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(16,24,40,0.06);
}}

.small-note {{
  color: #6b7280;
  font-size: 13px;
}}
</style>
"""

def render_header():
    """Pinta el header fijo con logo quesito y texto."""
    st.markdown(HEADER_CSS, unsafe_allow_html=True)
    header_html = f"""
    <div class="header-left" aria-hidden="true">
      <div style="width:44px;height:44px;display:flex;align-items:center;justify-content:center;">
        {CHEESE_SVG}
      </div>
      <div>
        <div class="header-title">Bienvenido a la Clínica Quesitos</div>
        <div class="header-sub">Tu veterinario de confianza</div>
      </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_hero():
    """Muestra la imagen hero (SVG) en la parte superior de la página."""
    st.markdown("<div class='main-with-header'></div>", unsafe_allow_html=True)
    st.markdown(HERO_SVG, unsafe_allow_html=True)
