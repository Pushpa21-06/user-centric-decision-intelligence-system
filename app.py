from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session
)

from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime


app = Flask(__name__)

app.secret_key = "decision_intelligence"

CORS(app)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =====================================
# GLOBAL STORAGE
# =====================================

history_data = []

current_analysis = {}


# =====================================
# PAGES
# =====================================

@app.route("/app")
def frontend():

    return render_template(
        "login.html"
    )


@app.route("/app/dashboard")
def dashboard():

    return render_template(
        "dashboard.html"
    )


@app.route("/app/results")
def results():

    return render_template(
        "results.html"
    )


# =====================================
# ANALYZE FILE
# =====================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    global current_analysis

    if "file" not in request.files:

        return jsonify({
            "error":
            "No file uploaded"
        })

    file = request.files["file"]

    mode = request.form.get(
        "mode",
        "auto"
    )

    x_axis = request.form.get(
        "x_axis"
    )

    y_axis = request.form.get(
        "y_axis"
    )

    filename = file.filename

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(path)

    # =====================
    # READ FILE
    # =====================

    if filename.endswith(
        ".csv"
    ):

        df = pd.read_csv(path)

    elif filename.endswith(
        ".xlsx"
    ):

        df = pd.read_excel(path)

    else:

        return jsonify({
            "error":
            "Invalid file"
        })

    columns = list(
        df.columns
    )

    # =====================
    # MANUAL MODE
    # ONLY RETURN COLUMNS
    # =====================

    if (
        mode == "manual"
        and
        (
            not x_axis
            or
            not y_axis
        )
    ):

        return jsonify({

            "columns":
            columns
        })

    # =====================
    # AUTO MODE
    # =====================

    numeric = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    text = [

        c for c in columns
        if c not in numeric
    ]

    if mode == "auto":

        x_axis = (
            text[0]
            if text
            else columns[0]
        )

        y_axis = (
            numeric[0]
            if numeric
            else columns[1]
        )

    # =====================
    # CHART DATA
    # =====================

    grouped = (
        df.groupby(x_axis)
        [y_axis]
        .sum()
        .reset_index()
    )

    labels = (
        grouped[x_axis]
        .astype(str)
        .tolist()
    )

    values = (
        grouped[y_axis]
        .tolist()
    )

    current_analysis = {

        "labels":
        labels,

        "values":
        values,

        "x_axis":
        x_axis,

        "y_axis":
        y_axis
    }

    history_data.insert(
        0,
        {

            "filename":
            filename,

            "time":
            datetime.now()
            .strftime(
                "%I:%M %p"
            ),

            "mode":
            mode.capitalize()
        }
    )

    return jsonify({

        "success":
        True
    })

    # ========================
    # READ FILE
    # ========================

    try:

        if filename.endswith(
            ".csv"
        ):

            df = pd.read_csv(
                filepath
            )

        elif filename.endswith(
            ".xlsx"
        ):

            df = pd.read_excel(
                filepath
            )

        else:

            return jsonify({
                "error":
                "Unsupported file"
            }), 400

    except Exception as e:

        return jsonify({
            "error":
            str(e)
        }), 500

    columns = list(df.columns)

    numeric_columns = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    text_columns = [
        col for col in columns
        if col not in
        numeric_columns
    ]

    # ========================
    # AUTO MODE
    # ========================

    if mode == "auto":

        x_axis = (
            text_columns[0]
            if text_columns
            else columns[0]
        )

        y_axis = (
            numeric_columns[0]
            if numeric_columns
            else columns[1]
        )

    # ========================
    # CREATE DATA
    # ========================

    grouped = (
        df.groupby(x_axis)
        [y_axis]
        .sum()
        .reset_index()
    )

    labels = (
        grouped[x_axis]
        .astype(str)
        .tolist()
    )

    values = (
        grouped[y_axis]
        .tolist()
    )

    current_analysis = {

        "labels":
        labels,

        "values":
        values,

        "x_axis":
        x_axis,

        "y_axis":
        y_axis
    }

    # ========================
    # HISTORY
    # ========================

    history_data.insert(
        0,
        {

            "filename":
            filename,

            "time":
            datetime.now()
            .strftime(
                "%I:%M %p"
            ),

            "mode":
            mode.capitalize()
        }
    )

    return jsonify({

        "success":
        True,

        "columns":
        columns,

        "x_axis":
        x_axis,

        "y_axis":
        y_axis
    })


# =====================================
# GET RESULT DATA
# =====================================

@app.route(
    "/get-results"
)
def get_results():

    return jsonify(
        current_analysis
    )


# =====================================
# GET HISTORY
# =====================================

@app.route(
    "/history"
)
def history():

    return jsonify(
        history_data
    )


# =====================================
# RUN APP
# =====================================

if __name__ == "__main__":

    app.run(
        debug=True
    )