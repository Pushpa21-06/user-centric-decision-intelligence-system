from flask import Blueprint, request, jsonify

from services.file_service import save_uploaded_file

upload_bp = Blueprint("upload_bp", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_file():

    # Check file exists
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file provided"
        }), 400

    file = request.files["file"]

    # Check filename
    if file.filename == "":
        return jsonify({
            "status": "error",
            "message": "Empty filename"
        }), 400

    try:
        result = save_uploaded_file(file)

        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500