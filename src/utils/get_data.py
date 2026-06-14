"""
Chargement des fichiers Excel FBI 2024 et stockage SQLite (table raw).
"""

import sqlite3
import pandas as pd
from config import DATA_DIR, FILES, SKIP_ROWS, DB_PATH


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


def _safe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rend les noms de colonnes compatibles SQLite (supprime sauts de ligne).

    Args:
        df: DataFrame source.

    Returns:
        DataFrame avec noms de colonnes normalisés.
    """
    df = df.copy()
    df.columns = [
        str(c).replace("\n", " ").strip() for c in df.columns
    ]
    return df


def save_raw_to_sqlite(raw: dict[str, pd.DataFrame], db_path: str = DB_PATH) -> None:
    """
    Persiste chaque table brute dans la base SQLite sous le préfixe ``raw_``.

    Args:
        raw:     dictionnaire {clé: DataFrame brut} retourné par load_all().
        db_path: chemin vers le fichier SQLite.
    """
    with sqlite3.connect(db_path) as conn:
        for key, df in raw.items():
            table_name = f"raw_{key}"
            safe = _safe_columns(df)
            safe.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"  → Données brutes sauvegardées dans {db_path}")


def load_raw_from_sqlite(db_path: str = DB_PATH) -> dict[str, pd.DataFrame]:
    """
    Relit les tables brutes depuis SQLite (préfixe ``raw_``).

    Args:
        db_path: chemin vers le fichier SQLite.

    Returns:
        Dictionnaire {clé: DataFrame}.  Colonnes renommées avec espaces.
    """
    result = {}
    with sqlite3.connect(db_path) as conn:
        for key in FILES:
            table_name = f"raw_{key}"
            result[key] = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    return result
