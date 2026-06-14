"""
Chargement des fichiers Excel du FBI Hate Crime Statistics 2024.
"""

import pandas as pd
from config import DATA_DIR, FILES, SKIP_ROWS


def load(filename: str, skip_rows: int) -> pd.DataFrame:
    """
    Charge un fichier Excel en sautant les en-têtes FBI multi-lignes.

    Args:
        filename:  nom du fichier dans DATA_DIR.
        skip_rows: nombre de lignes d'en-tête à ignorer.

    Returns:
        DataFrame nettoyé avec colonnes typées.
    """
    path = DATA_DIR + filename
    df = pd.read_excel(path, skiprows=skip_rows, header=None)

    # Supprimer lignes entièrement vides et notes de bas de page
    df = df.dropna(how="all")
    df = df[df.iloc[:, 0].notna()]

    # Noms de colonnes à partir de la première ligne de données
    df.columns = df.iloc[0]
    df = df[1:]

    # Supprimer les lignes qui commencent par un chiffre (notes de bas de page)
    df = df[~df.iloc[:, 0].astype(str).str.match(r"^\d+\s")]

    # Conversion numérique des colonnes non-clé
    df[df.columns[1:]] = (
        df[df.columns[1:]]
        .apply(pd.to_numeric, errors="coerce")
        .astype("Int64")
    )

    return df


def load_all() -> dict[str, pd.DataFrame]:
    """
    Charge les cinq tables utilisées dans l'analyse.

    Returns:
        Dictionnaire {clé: DataFrame brut}.
    """
    return {
        key: load(FILES[key], SKIP_ROWS[key])
        for key in FILES
    }