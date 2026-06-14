"""
Main entry point - FBI Hate Crime Statistics 2024.
Runs the data pipeline and starts the interactive Dash dashboard.

Usage:
    python main.py
"""

import os
import warnings
warnings.filterwarnings("ignore")

from config import DB_PATH, DASH_HOST, DASH_PORT, DASH_DEBUG
from src.utils.get_data   import load_all, save_raw_to_sqlite
from src.utils.clean_data import (
    clean_t1, clean_t2, clean_t9, clean_t10, clean_t12,
    save_cleaned_to_sqlite,
)
from src.pages.summary    import render_summary
from src.dash_app.app     import app
from src.pages.home       import build_layout
from src.dash_app.callbacks import register_callbacks


def _build_data() -> dict:
    """
    Charge et nettoie les données FBI, les persiste dans SQLite.

    Returns:
        Dictionnaire de DataFrames nettoyés prêts pour le dashboard.
    """
    # ── 1. Chargement ─────────────────────────────────────────────────────
    raw = load_all()
    save_raw_to_sqlite(raw, DB_PATH)
    print("Données brutes chargées et sauvegardées en base.")

    # ── 2. Nettoyage ──────────────────────────────────────────────────────
    t1_detail, t1   = clean_t1(raw["t1"])
    t2_clean        = clean_t2(raw["t2"])
    t9_race, _      = clean_t9(raw["t9"])
    t10_locations   = clean_t10(raw["t10"])
    t12_states      = clean_t12(raw["t12"])

    data = dict(
        t1_detail=t1_detail, t1=t1,
        t2_clean=t2_clean,
        t9_race=t9_race,
        t10_locations=t10_locations,
        t12_states=t12_states,
    )
    save_cleaned_to_sqlite(data, DB_PATH)
    print("Données nettoyées sauvegardées en base.")

    # ── 3. Résumé console ─────────────────────────────────────────────────
    render_summary(t1_detail)
    return data


def main() -> None:
    """Run the data pipeline and start the Dash server."""
    data = _build_data()

    # 4. Dash layout
    app.layout = build_layout()

    # 5. Callbacks (interactivity)
    register_callbacks(data)

    # 6. Start server
    print(f"\nDashboard available at http://{DASH_HOST}:{DASH_PORT}")
    app.run(host=DASH_HOST, port=DASH_PORT, debug=DASH_DEBUG)


if __name__ == "__main__":
    main()
