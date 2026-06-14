"""
Point d'entrée principal — FBI Hate Crime Statistics 2024.
Lance le chargement, le nettoyage et la génération des visualisations.
"""

import warnings
warnings.filterwarnings("ignore")

from src.utils.get_data        import load_all
from src.utils.clean_data      import clean_t1, clean_t2, clean_t9, clean_t10, clean_t12
from src.utils.common_functions import apply_mpl_style, print_complementary_analyses
from src.pages.summary         import render_summary
from src.pages.home            import render_home, save_home


def main() -> None:
    apply_mpl_style()

    # ── 1. Chargement ─────────────────────────────────────────────────────
    raw = load_all()
    print("Données chargées")

    # ── 2. Nettoyage ──────────────────────────────────────────────────────
    t1_detail, t1     = clean_t1(raw["t1"])
    t2_clean          = clean_t2(raw["t2"])
    t9_race, t9_eth   = clean_t9(raw["t9"])
    t10_locations     = clean_t10(raw["t10"])
    t12_states        = clean_t12(raw["t12"])

    print(f"\n  • Table 1  – {len(t1_detail)} motivations de biais détaillées")
    print(f"  • Table 2  – {len(t2_clean)} types d'infractions")
    print(f"  • Table 9  – Profil de {int(t9_race['Total'].sum())} auteurs connus (race)")
    print(f"  • Table 12 – {len(t12_states)} États analysés")
    print(f"  • Table 10 – {len(t10_locations)} lieux recensés")

    # ── 3. Résumé national ────────────────────────────────────────────────
    render_summary(t1_detail)

    # ── 4. Visualisations ─────────────────────────────────────────────────
    data = dict(
        t1_detail=t1_detail, t1=t1,
        t2_clean=t2_clean,
        t9_race=t9_race,
        t10_locations=t10_locations,
        t12_states=t12_states,
    )
    fig = render_home(data)
    save_home(fig)

    # ── 5. Analyses complémentaires ───────────────────────────────────────
    total_row = t1_detail[t1_detail["Bias motivation"] == "Total"].iloc[0]
    print_complementary_analyses(t12_states, t2_clean, total_row)


if __name__ == "__main__":
    main()