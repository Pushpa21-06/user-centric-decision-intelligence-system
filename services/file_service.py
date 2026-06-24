import os
import pandas as pd

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"csv", "xlsx"}

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_uploaded_file(file):

    # Validate file extension
    if not allowed_file(file.filename):

        raise Exception(
            "Unsupported file type. Only CSV and XLSX are allowed."
        )

    # Secure filename
    filename = secure_filename(file.filename)

    # Full file path
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save file
    file.save(filepath)

    # Extract metadata
    metadata = extract_file_metadata(filepath)

    return {
        "filename": filename,
        "filepath": filepath,
        "metadata": metadata
    }


def extract_file_metadata(filepath):

    extension = filepath.rsplit(".", 1)[1].lower()

    # CSV FILE HANDLING
    if extension == "csv":

        df = pd.read_csv(filepath)

        columns = df.columns.tolist()

        numeric_columns = (
            df.select_dtypes(include=["number"])
            .columns
            .tolist()
        )

        return {
            "file_type": "csv",
            "sheets": ["CSV_Data"],
            "columns": {
                "CSV_Data": columns
            },
            "numeric_columns": {
                "CSV_Data": numeric_columns
            }
        }

    # EXCEL FILE HANDLING
    elif extension == "xlsx":

        excel_file = pd.ExcelFile(
        filepath,
        engine="openpyxl"
)
        sheets = excel_file.sheet_names

        columns_data = {}
        numeric_data = {}

        for sheet in sheets:

            df = pd.read_excel(
    filepath,
    sheet_name=sheet,
    engine="openpyxl"
)

            columns_data[sheet] = df.columns.tolist()

            numeric_data[sheet] = (
                df.select_dtypes(include=["number"])
                .columns
                .tolist()
            )

        return {
            "file_type": "excel",
            "sheets": sheets,
            "columns": columns_data,
            "numeric_columns": numeric_data
        }

    else:

        raise Exception("Unsupported file format")