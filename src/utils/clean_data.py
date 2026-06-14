"""
Nettoyage et transformation des tables brutes FBI 2024.
"""

import pandas as pd
from config import AGGREGATED_BIASES, EXCLUDE_STATES


def clean_t1(t1_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Table 1 – Motivations de biais.

    Returns:
        (t1_detail, t1) : table complète et table sans lignes agrégées.
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
    t10_locations = (
        t10[["Location", "Total\nincidents"]]
        .copy()
        .sort_values("Total\nincidents", ascending=False)
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

    t12_states["incidents_per_100k"] = (
        t12_states["Total\nnumber of\nincidents\nreported"]
        / t12_states["Population\ncovered"]
        * 100_000
    ).round(2)

    t12_states["reporting_rate"] = (
        t12_states["Agencies\nsubmitting\nincident\nreports"]
        / t12_states["Number of\nparticipating\nagencies"]
        * 100
    ).round(1)

    return t12_states