"""
Configuration globale du projet FBI Hate Crime Statistics 2024.
"""

import os

# ── Chemins ────────────────────────────────────────────────────────────────
DATA_DIR    = "data/hate_crime_2024/"
IMAGES_DIR  = "images/"
OUTPUT_PNG  = "images/hate_crime_2024_analyse.png"
DB_PATH     = "data/db.sqlite"

# ── Dash ───────────────────────────────────────────────────────────────────
DASH_HOST   = "127.0.0.1"
DASH_PORT   = 8050
DASH_DEBUG  = False

# ── Palette de couleurs ────────────────────────────────────────────────────
COLORS = {
    "primary":   "#C0392B",
    "secondary": "#2C3E50",
    "accent":    "#E67E22",
    "neutral":   "#7F8C8D",
    "highlight": "#2980B9",
    "palette":   ["#C0392B", "#2980B9", "#27AE60", "#E67E22", "#8E44AD", "#16A085"],
}

# ── Paramètres matplotlib (toujours utilisé pour export PNG si besoin) ─────
MPL_PARAMS = {
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor":   "#FAFAFA",
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   13,
    "axes.labelsize":   11,
}

# ── Métadonnées nationales ─────────────────────────────────────────────────
NUM_AGENCIES  = 16_419
POP_COVERED   = 323_341_545

# ── Noms des fichiers sources ──────────────────────────────────────────────
FILES = {
    "t1":  "Hate_Crime_Table_1_Incidents_Offenses_Victims_and_Known_Offenders_by_Bias_Motivation_2024.xlsx",
    "t2":  "Hate_Crime_Table_2_Incidents_Offenses_Victims_and_Known_Offenders_by_Offense_Type_2024.xlsx",
    "t9":  "Hate_Crime_Table_9_Known_Offenders_Known_Offenders_Race_Ethnicity_and_Age_2024.xlsx",
    "t10": "Hate_Crime_Table_10_Incidents_Bias_Motivation_by_Location_2024.xlsx",
    "t12": "Hate_Crime_Table_12_Agency_Hate_Crime_Reporting_by_State_and_Federal_2024.xlsx",
}

# ── Lignes d'en-tête à ignorer par table ──────────────────────────────────
SKIP_ROWS = {"t1": 3, "t2": 3, "t9": 3, "t10": 5, "t12": 2}

# ── Regroupements à exclure des analyses détaillées ───────────────────────
AGGREGATED_BIASES = [
    "Total", "Single-Bias Incidents", "Multiple-Bias Incidents",
    "Race/Ethnicity/Ancestry:", "Religion:", "Sexual Orientation:",
    "Disability:", "Gender:", "Gender Identity:",
]

EXCLUDE_STATES = [
    "Total", "Bureau of Indian Affairs", "Federal",
    "Guam", "Puerto Rico", "U.S. Virgin Islands",
]
