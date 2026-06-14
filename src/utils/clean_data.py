"""
Cleaning and transformation of raw FBI 2024 tables.
Also stores cleaned data in SQLite (table cleaned_*).
"""

import sqlite3
import pandas as pd
from config import AGGREGATED_BIASES, EXCLUDE_STATES, DB_PATH


# Data cleaning functions

def clean_t1(t1_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Table 1 - Bias motivations.

    Returns:
        (t1_detail, t1) : complete table and table without aggregated rows.
    """
    t1_detail = t1_raw.dropna()
    t1 = t1_detail[~t1_detail["Bias motivation"].isin(AGGREGATED_BIASES)]
    return t1_detail, t1


def clean_t2(t2_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Table 2 – Types d'infractions.
    Conserve uniquement les types spécifiques (retire totaux et catégories).
    """
    t2 = t2_raw.dropna(axis=1, how="all")
    t2_clean = t2[
        ~t2["Offense type"].str.contains(r"(?i)total|crimes against", na=True)
    ].copy()
    return t2_clean


def clean_t9(t9_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Table 9 – Profil des auteurs connus.
    Lignes 0-6 = race, 7-11 = ethnie, 12+ = âge.

    Returns:
        (t9_race, t9_eth) : sous-tables race et ethnicité.
    """
    t9 = t9_raw.loc[
        :, t9_raw.columns.notna() & (t9_raw.columns != "")
    ].dropna()
    t9_race = t9.iloc[1:7].copy()
    t9_eth  = t9.iloc[8:12].copy()
    return t9_race, t9_eth


def clean_t10(t10_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Table 10 – Lieux d'incidents.
    Garde uniquement les colonnes lieu + total, triées par volume décroissant.
    """
    t10 = t10_raw.dropna()
    # Compatibilité : la colonne peut avoir un saut de ligne ou un espace
    loc_col = next(
        (c for c in t10.columns if "total" in c.lower() and "incident" in c.lower()),
        None,
    )
    if loc_col is None:
        loc_col = t10.columns[1]
    t10_locations = (
        t10[["Location", loc_col]]
        .rename(columns={loc_col: "Total incidents"})
        .copy()
        .sort_values("Total incidents", ascending=False)
    )
    return t10_locations


def clean_t12(t12_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Table 12 – Signalement par État.
    Ajoute les taux incidents/100k et taux de signalement des agences.
    """
    t12 = t12_raw.dropna()
    t12_states = t12[
        ~t12["Participating State/Federal"].isin(EXCLUDE_STATES)
    ].copy()

    # Colonnes normalisées (les sauts de ligne ont été retirés dans get_data)
    inc_col = next(
        (c for c in t12_states.columns if "incident" in c.lower() and "total" in c.lower()),
        None,
    )
    pop_col = next(
        (c for c in t12_states.columns if "population" in c.lower()), None
    )
    agencies_col = next(
        (c for c in t12_states.columns if "submitting" in c.lower()), None
    )
    part_col = next(
        (c for c in t12_states.columns if "participating" in c.lower() and "number" in c.lower()),
        None,
    )

    if inc_col and pop_col:
        t12_states["incidents_per_100k"] = (
            pd.to_numeric(t12_states[inc_col], errors="coerce")
            / pd.to_numeric(t12_states[pop_col], errors="coerce")
            * 100_000
        ).round(2)

    if agencies_col and part_col:
        t12_states["reporting_rate"] = (
            pd.to_numeric(t12_states[agencies_col], errors="coerce")
            / pd.to_numeric(t12_states[part_col], errors="coerce")
            * 100
        ).round(1)

    # Standardiser le nom de la colonne incidents totaux
    if inc_col:
        t12_states = t12_states.rename(columns={inc_col: "Total incidents reported"})

    return t12_states


# ──────────────────────────────────────────────────────────────────────────
# Persistance SQLite
# ──────────────────────────────────────────────────────────────────────────

def _safe_df(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit Int64 → float pour compatibilité SQLite."""
    return df.astype(
        {c: "float" for c in df.columns if hasattr(df[c], "dtype") and str(df[c].dtype) == "Int64"}
    )


def save_cleaned_to_sqlite(cleaned: dict[str, pd.DataFrame], db_path: str = DB_PATH) -> None:
    """
    Persiste chaque DataFrame nettoyé dans SQLite sous le préfixe ``cleaned_``.

    Args:
        cleaned: dict {nom: DataFrame}.
        db_path: chemin vers le fichier SQLite.
    """
    with sqlite3.connect(db_path) as conn:
        for name, df in cleaned.items():
            _safe_df(df).to_sql(f"cleaned_{name}", conn, if_exists="replace", index=False)
    print(f"  → Données nettoyées sauvegardées dans {db_path}")


def load_cleaned_from_sqlite(db_path: str = DB_PATH) -> dict[str, pd.DataFrame]:
    """
    Relit les tables nettoyées depuis SQLite.

    Args:
        db_path: chemin vers le fichier SQLite.

    Returns:
        dict {nom: DataFrame}.
    """
    tables = [
        "t1_detail", "t1", "t2_clean",
        "t9_race", "t10_locations", "t12_states",
    ]
    result = {}
    with sqlite3.connect(db_path) as conn:
        for name in tables:
            result[name] = pd.read_sql(f"SELECT * FROM cleaned_{name}", conn)
    return result
