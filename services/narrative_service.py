def generate_narrative(df, x_column, y_column):

    # Highest value row
    highest_row = df.loc[df[y_column].idxmax()]

    # Lowest value row
    lowest_row = df.loc[df[y_column].idxmin()]

    # Average value
    average_value = round(df[y_column].mean(), 2)

    # Total value
    total_value = round(df[y_column].sum(), 2)

    # Insights
    insights = (
        f"The dataset contains a total value of "
        f"{total_value} across all records. "
        f"The average {y_column} is {average_value}. "
        f"The highest contribution comes from "
        f"{highest_row[x_column]} with a value of "
        f"{highest_row[y_column]}. "
        f"The lowest contribution comes from "
        f"{lowest_row[x_column]} with a value of "
        f"{lowest_row[y_column]}."
    )

    # Analysis
    analysis = (
        f"The analysis indicates that "
        f"{highest_row[x_column]} dominates the dataset "
        f"compared to other categories. "
        f"There is a noticeable variation between "
        f"the highest and lowest values, suggesting "
        f"an uneven distribution pattern in the data."
    )

    # Recommendation
    recommendation = (
        f"It is recommended to closely monitor "
        f"{highest_row[x_column]} since it represents "
        f"the largest share of the dataset. "
        f"Optimizing or balancing the distribution "
        f"may improve overall efficiency and stability."
    )

    return {
        "insights": insights,
        "analysis": analysis,
        "recommendation": recommendation
    }