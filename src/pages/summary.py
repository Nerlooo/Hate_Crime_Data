"""
Page simple : résumé national des statistiques 2024.
"""

import pandas as pd
from src.utils.common_functions import print_national_summary


def render_summary(t1_detail: pd.DataFrame) -> None:
    """
    Affiche le résumé national dans la console.

    Args:
        t1_detail: DataFrame complet de la Table 1.
    """
    total_row = t1_detail[t1_detail["Bias motivation"] == "Total"].iloc[0]
    print_national_summary(total_row)