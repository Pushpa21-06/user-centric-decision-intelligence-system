import plotly.express as px


def generate_bar_chart(df, x_column, y_column):

    figure = px.bar(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} by {x_column}"
    )

    return figure.to_json()