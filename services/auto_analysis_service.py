from services.history_service import save_analysis_history
from services.narrative_service import generate_narrative
import pandas as pd

from services.visualization_service import generate_bar_chart


def run_auto_analysis(filepath):

    extension = filepath.rsplit(".", 1)[1].lower()

    # CSV FILE
    if extension == "csv":

        df = pd.read_csv(filepath)

    # EXCEL FILE
    else:

        df = pd.read_excel(
    filepath,
    engine="openpyxl"
)

    # Detect numeric columns
    numeric_columns = (
        df.select_dtypes(include=["number"])
        .columns
        .tolist()
    )

    # Ensure enough columns
    if len(numeric_columns) < 1:

        raise Exception(
            "No numeric columns available for analysis."
        )

    # Select columns automatically
    y_column = numeric_columns[0]

    # Choose first non-numeric column for x-axis
    non_numeric_columns = (
        df.select_dtypes(exclude=["number"])
        .columns
        .tolist()
    )

    if len(non_numeric_columns) > 0:

        x_column = non_numeric_columns[0]

    else:

        x_column = df.columns[0]

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
    "mode": "auto",
    "x_column": x_column,
    "y_column": y_column,
    "insights": narrative["insights"],
    "analysis": narrative["analysis"],
    "recommendation": narrative["recommendation"]
})
    return {
    "mode": "auto",
    "x_column": x_column,
    "y_column": y_column,
    "chart": chart_json,
    "insights": narrative["insights"],
    "analysis": narrative["analysis"],
    "recommendation": narrative["recommendation"]
}