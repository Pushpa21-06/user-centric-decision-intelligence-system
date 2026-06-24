from services.history_service import save_analysis_history
from services.narrative_service import generate_narrative
import pandas as pd

from services.visualization_service import generate_bar_chart


def run_manual_analysis(
    filepath,
    sheet_name,
    x_column,
    y_column
):

    extension = filepath.rsplit(".", 1)[1].lower()

    # CSV FILE
    if extension == "csv":

        df = pd.read_csv(filepath)

    # EXCEL FILE
    else:

       df = pd.read_excel(
    filepath,
    sheet_name=sheet_name,
    engine="openpyxl"
)

    # Validate x column
    if x_column not in df.columns:

        raise Exception(
            f"{x_column} column not found."
        )

    # Validate y column
    if y_column not in df.columns:

        raise Exception(
            f"{y_column} column not found."
        )

    # Generate chart
    chart_json = generate_bar_chart(
        df,
        x_column,
        y_column
    )
    # Generate narrative
    narrative = generate_narrative(
    df,
    x_column,
    y_column
)
# Save history
    save_analysis_history({
    "mode": "manual",
    "x_column": x_column,
    "y_column": y_column,
    "insights": narrative["insights"],
    "analysis": narrative["analysis"],
    "recommendation": narrative["recommendation"]
})
    return {
    "mode": "manual",
    "x_column": x_column,
    "y_column": y_column,
    "chart": chart_json,
    "insights": narrative["insights"],
    "analysis": narrative["analysis"],
    "recommendation": narrative["recommendation"]
}