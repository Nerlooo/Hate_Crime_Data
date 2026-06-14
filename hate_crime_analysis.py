"""
FBI Hate Crime Statistics 2024 - Analyse complète
Source : FBI Uniform Crime Reporting Program
Données : 14 tableaux XLSX couvrant les crimes haineux signalés aux États-Unis en 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Configuration ─────────────────────────────────────────────────────────────
DATA_DIR = "./hate_crime_data/hate_crime_2024/"   # <-- adapter si besoin

plt.rcParams.update({
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor": "#FAFAFA",
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})

COLORS = {
    "primary":   "#C0392B",
    "secondary": "#2C3E50",
    "accent":    "#E67E22",
    "neutral":   "#7F8C8D",
    "highlight": "#2980B9",
    "palette":   ["#C0392B","#2980B9","#27AE60","#E67E22","#8E44AD","#16A085"],
}

def load(filename, skip_rows, col_names):
    """Charge un fichier XLSX en sautant les en-têtes FBI multi-lignes."""
    path = DATA_DIR + filename
    df = pd.read_excel(path, skiprows=skip_rows, header=None, names=col_names)
    # Supprimer lignes entièrement vides et notes de bas de page
    df = df.dropna(how="all")
    df = df[df.iloc[:, 0].notna()]
    # Retirer les lignes qui commencent par un chiffre (notes de bas de page)
    df = df[~df.iloc[:, 0].astype(str).str.match(r"^\d+\s")]
    return df


# ══════════════════════════════════════════════════════════════════════════════
# 1. CHARGEMENT DES DONNÉES
# ══════════════════════════════════════════════════════════════════════════════

# --- Table 1 : incidents / motivations de biais ---------------------------
t1_cols = ["bias_motivation", "incidents", "offenses", "victims", "known_offenders"]
t1 = load(
    "Hate_Crime_Table_1_Incidents_Offenses_Victims_and_Known_Offenders_by_Bias_Motivation_2024.xlsx",
    skip_rows=4,
    col_names=t1_cols[:5] + [f"extra_{i}" for i in range(5)],
)
t1 = t1[t1_cols[:5]].copy()
t1[["incidents","offenses","victims","known_offenders"]] = (
    t1[["incidents","offenses","victims","known_offenders"]].apply(pd.to_numeric, errors="coerce")
)
t1 = t1[t1["incidents"].notna()]

# Séparer lignes agrégées / détail
AGGREGATED = ["Total","Single-Bias Incidents","Multiple-Bias Incidents",
              "Race/Ethnicity/Ancestry:","Religion:","Sexual Orientation:",
              "Disability:","Gender:","Gender Identity:"]
t1_detail = t1[~t1["bias_motivation"].isin(AGGREGATED)].copy()

# --- Table 2 : types d'infractions ----------------------------------------
t2_cols = ["offense_type","incidents","offenses","victims","known_offenders"]
t2 = load(
    "Hate_Crime_Table_2_Incidents_Offenses_Victims_and_Known_Offenders_by_Offense_Type_2024.xlsx",
    skip_rows=4,
    col_names=t2_cols + [f"x{i}" for i in range(3)],
)
t2 = t2[t2_cols].copy()
t2[t2_cols[1:]] = t2[t2_cols[1:]].apply(pd.to_numeric, errors="coerce")
t2 = t2[t2["offenses"].notna()]
t2_clean = t2[~t2["offense_type"].str.contains(r"(?i)total|crimes against", na=True)].copy()
t2_clean["offense_type"] = t2_clean["offense_type"].str.strip()

# --- Table 9 : profil des auteurs connus -----------------------------------
t9_raw = pd.read_excel(
    DATA_DIR + "Hate_Crime_Table_9_Known_Offenders_Known_Offenders_Race_Ethnicity_and_Age_2024.xlsx",
    skiprows=3, header=None
)
# Lignes 0-6 = race, 7-11 = ethnie, 12+ = âge
t9_raw.columns = ["category","count","pct"]
t9_raw = t9_raw.dropna(subset=["category"])
t9_raw["count"] = pd.to_numeric(t9_raw["count"], errors="coerce")
t9_race = t9_raw.iloc[1:7].copy()
t9_eth  = t9_raw.iloc[8:12].copy()

# --- Table 12 : signalement par État ---------------------------------------
t12_cols = ["state","num_agencies","population","agencies_reporting","incidents_reported","x"]
t12 = load(
    "Hate_Crime_Table_12_Agency_Hate_Crime_Reporting_by_State_and_Federal_2024.xlsx",
    skip_rows=3,
    col_names=t12_cols,
)
t12 = t12[t12_cols[:5]].copy()
t12[t12_cols[1:5]] = t12[t12_cols[1:5]].apply(pd.to_numeric, errors="coerce")
t12 = t12[t12["incidents_reported"].notna()]
# Garder uniquement les États (retirer Total, fédéral, territoires)
EXCLUDE_STATES = ["Total","Bureau of Indian Affairs","Federal","Guam",
                  "Puerto Rico","U.S. Virgin Islands"]
t12_states = t12[~t12["state"].isin(EXCLUDE_STATES)].copy()
t12_states = t12_states[t12_states["state"].str.match(r"^[A-Z][a-z]", na=False)]
t12_states["incidents_per_100k"] = (
    t12_states["incidents_reported"] / t12_states["population"] * 100_000
).round(2)
t12_states["reporting_rate"] = (
    t12_states["agencies_reporting"] / t12_states["num_agencies"] * 100
).round(1)

# --- Table 10 : lieux d'incidents ------------------------------------------
t10_raw = pd.read_excel(
    DATA_DIR + "Hate_Crime_Table_10_Incidents_Bias_Motivation_by_Location_2024.xlsx",
    skiprows=6, header=None
)
t10_raw.columns = ["location","total"] + [f"c{i}" for i in range(t10_raw.shape[1]-2)]
t10_raw["total"] = pd.to_numeric(t10_raw["total"], errors="coerce")
t10_raw = t10_raw[t10_raw["total"].notna() & t10_raw["location"].notna()]
t10_raw = t10_raw[~t10_raw["location"].astype(str).str.match(r"^\d")]
t10_locations = t10_raw[["location","total"]].copy().sort_values("total", ascending=False)
t10_locations = t10_locations[t10_locations["location"].str.strip() != "Total"]

print("✅ Données chargées avec succès !\n")
print(f"  • Table 1  – {len(t1_detail)} motivations de biais détaillées")
print(f"  • Table 2  – {len(t2_clean)} types d'infractions")
print(f"  • Table 9  – Profil de {int(t9_race['count'].sum())} auteurs connus (race)")
print(f"  • Table 12 – {len(t12_states)} États analysés")
print(f"  • Table 10 – {len(t10_locations)} lieux recensés")


# ══════════════════════════════════════════════════════════════════════════════
# 2. STATISTIQUES RÉSUMÉ
# ══════════════════════════════════════════════════════════════════════════════

total_row = t1[t1["bias_motivation"] == "Total"].iloc[0]
print("\n" + "═"*55)
print("  RÉSUMÉ NATIONAL 2024")
print("═"*55)
print(f"  Incidents totaux       : {int(total_row['incidents']):>8,}")
print(f"  Infractions totales    : {int(total_row['offenses']):>8,}")
print(f"  Victimes totales       : {int(total_row['victims']):>8,}")
print(f"  Auteurs connus         : {int(total_row['known_offenders']):>8,}")
print(f"  Agences participantes  : {16419:>8,}")
print(f"  Population couverte    : {323_341_545:>8,}")
print("═"*55)


# ══════════════════════════════════════════════════════════════════════════════
# 3. VISUALISATIONS
# ══════════════════════════════════════════════════════════════════════════════

fig = plt.figure(figsize=(22, 28))
fig.suptitle(
    "FBI Hate Crime Statistics 2024 — Analyse Complète",
    fontsize=20, fontweight="bold", color=COLORS["secondary"], y=0.98
)

gs = fig.add_gridspec(4, 2, hspace=0.45, wspace=0.35)


# ── 3.1 Top 15 motivations de biais ────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :])
top15 = t1_detail.nlargest(15, "incidents").sort_values("incidents")
bar_colors = [COLORS["primary"] if i >= 10 else COLORS["secondary"] for i in range(len(top15))]
bars = ax1.barh(top15["bias_motivation"], top15["incidents"], color=bar_colors, edgecolor="white")
for bar in bars:
    w = bar.get_width()
    ax1.text(w + 15, bar.get_y() + bar.get_height()/2,
             f"{int(w):,}", va="center", fontsize=9)
ax1.set_xlabel("Nombre d'incidents")
ax1.set_title("Top 15 des motivations de biais (incidents, 2024)", fontweight="bold")
ax1.set_xlim(0, top15["incidents"].max() * 1.15)
ax1.axvline(x=500, color=COLORS["accent"], lw=1, ls="--", alpha=0.5)
patch1 = mpatches.Patch(color=COLORS["primary"], label="Top 5")
patch2 = mpatches.Patch(color=COLORS["secondary"], label="6e–15e")
ax1.legend(handles=[patch1, patch2], loc="lower right")


# ── 3.2 Types d'infractions ────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 0])
top_off = t2_clean.nlargest(10, "offenses").sort_values("offenses")
palette2 = sns.color_palette("Reds_r", len(top_off))
ax2.barh(top_off["offense_type"], top_off["offenses"], color=palette2)
for i, (_, row) in enumerate(top_off.iterrows()):
    ax2.text(row["offenses"] + 20, i, f"{int(row['offenses']):,}", va="center", fontsize=8.5)
ax2.set_title("Types d'infractions (top 10)", fontweight="bold")
ax2.set_xlabel("Nombre d'infractions")


# ── 3.3 Catégories de biais ────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 1])
categories = {
    "Race/Ethnicité/\nAncestralité": t1[t1["bias_motivation"]=="Race/Ethnicity/Ancestry:"]["incidents"].values[0],
    "Religion":                      t1[t1["bias_motivation"]=="Religion:"]["incidents"].values[0],
    "Orientation\nsexuelle":         t1[t1["bias_motivation"]=="Sexual Orientation:"]["incidents"].values[0],
    "Identité\nde genre":            t1[t1["bias_motivation"]=="Gender Identity:"]["incidents"].values[0],
    "Handicap":                      t1[t1["bias_motivation"]=="Disability:"]["incidents"].values[0],
    "Genre":                         t1[t1["bias_motivation"]=="Gender:"]["incidents"].values[0],
}
cats = pd.Series(categories).sort_values(ascending=False)
wedge_colors = COLORS["palette"]
wedges, texts, autotexts = ax3.pie(
    cats.values, labels=cats.index, autopct="%1.1f%%",
    colors=wedge_colors, startangle=140,
    textprops={"fontsize": 8.5},
    pctdistance=0.78,
)
for at in autotexts:
    at.set_fontsize(8)
ax3.set_title("Répartition par grande catégorie de biais", fontweight="bold")


# ── 3.4 Top 15 États (incidents pour 100k habitants) ───────────────────────
ax4 = fig.add_subplot(gs[2, :])
top_states = t12_states.nlargest(15, "incidents_per_100k").sort_values("incidents_per_100k")
bar_colors4 = [COLORS["highlight"] if v > 5 else COLORS["secondary"] for v in top_states["incidents_per_100k"]]
ax4.barh(top_states["state"], top_states["incidents_per_100k"], color=bar_colors4)
for i, (_, row) in enumerate(top_states.iterrows()):
    ax4.text(row["incidents_per_100k"] + 0.05, i,
             f"{row['incidents_per_100k']:.1f}", va="center", fontsize=9)
ax4.set_xlabel("Incidents pour 100 000 habitants")
ax4.set_title("Top 15 États — Taux de crimes haineux pour 100 000 hab.", fontweight="bold")
patch_h = mpatches.Patch(color=COLORS["highlight"], label="> 5 pour 100k")
patch_s = mpatches.Patch(color=COLORS["secondary"], label="≤ 5 pour 100k")
ax4.legend(handles=[patch_h, patch_s], loc="lower right")


# ── 3.5 Profil racial des auteurs connus ───────────────────────────────────
ax5 = fig.add_subplot(gs[3, 0])
race_labels = t9_race["category"].str.strip().tolist()
race_vals   = t9_race["count"].tolist()
total_race  = sum(race_vals)
pcts = [v/total_race*100 for v in race_vals]
bars5 = ax5.bar(range(len(race_labels)), race_vals, color=COLORS["palette"], edgecolor="white")
ax5.set_xticks(range(len(race_labels)))
ax5.set_xticklabels(
    [l.replace(" or ", "\nor ").replace(" and ", "\nand ") for l in race_labels],
    fontsize=7.5, rotation=15, ha="right"
)
for i, (v, p) in enumerate(zip(race_vals, pcts)):
    ax5.text(i, v + 30, f"{int(v):,}\n({p:.1f}%)", ha="center", fontsize=7.5)
ax5.set_ylabel("Nombre d'auteurs")
ax5.set_title("Race des auteurs connus (Table 9)", fontweight="bold")


# ── 3.6 Lieux d'incidents (top 12) ─────────────────────────────────────────
ax6 = fig.add_subplot(gs[3, 1])
top_loc = t10_locations.head(12).sort_values("total")
palette6 = sns.color_palette("Blues_r", len(top_loc))
ax6.barh(top_loc["location"].str.strip(), top_loc["total"], color=palette6)
for i, (_, row) in enumerate(top_loc.iterrows()):
    ax6.text(row["total"] + 5, i, f"{int(row['total']):,}", va="center", fontsize=8.5)
ax6.set_xlabel("Incidents")
ax6.set_title("Lieux les plus fréquents (top 12)", fontweight="bold")


# ── Légende générale ────────────────────────────────────────────────────────
fig.text(0.5, 0.01,
         "Source : FBI Uniform Crime Reporting — Hate Crime Statistics 2024  |  "
         "16 419 agences participantes  |  Population couverte : 323 341 545",
         ha="center", fontsize=9, color=COLORS["neutral"])

plt.savefig("/mnt/user-data/outputs/hate_crime_2024_analyse.png",
            dpi=150, bbox_inches="tight")
print("\n✅ Graphique sauvegardé → hate_crime_2024_analyse.png")


# ══════════════════════════════════════════════════════════════════════════════
# 4. ANALYSES COMPLÉMENTAIRES (texte)
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "═"*55)
print("  ANALYSES COMPLÉMENTAIRES")
print("═"*55)

# Taux de signalement
avg_report = t12_states["reporting_rate"].mean()
top5_report = t12_states.nlargest(5, "reporting_rate")[["state","reporting_rate"]]
print(f"\n📍 Taux moyen de signalement des agences : {avg_report:.1f}%")
print("  États avec le meilleur taux de signalement :")
print(top5_report.to_string(index=False))

# Top 10 États absolus
print("\n📊 Top 10 États par nombre absolu d'incidents :")
top10_abs = t12_states.nlargest(10,"incidents_reported")[["state","incidents_reported","incidents_per_100k"]]
print(top10_abs.to_string(index=False))

# Infractions les plus violentes
violent = ["Murder and nonnegligent manslaughter","Rape","Aggravated assault","Robbery"]
t2_violent = t2_clean[t2_clean["offense_type"].isin(violent)]
print(f"\n⚠️  Infractions violentes (persons) : {t2_violent['offenses'].sum():.0f} infractions")

# Ratio victimes/incident
victims_total = int(total_row["victims"])
incidents_total = int(total_row["incidents"])
print(f"\n👥 Ratio moyen victimes/incident : {victims_total/incidents_total:.2f}")

print("\n✅ Analyse terminée.")
