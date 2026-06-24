from flask import Blueprint, request, jsonify

from services.auto_analysis_service import run_auto_analysis
from services.manual_analysis_service import run_manual_analysis

analyze_bp = Blueprint("analyze_bp", __name__)


@analyze_bp.route("/analyze", methods=["POST"])
def analyze_file():

    try:

        data = request.get_json()

        filepath = data.get("filepath")
        mode = data.get("mode")

        # AUTO MODE
        if mode == "auto":

            result = run_auto_analysis(filepath)

        # MANUAL MODE
        elif mode == "manual":

            result = run_manual_analysis(
                filepath=filepath,
                sheet_name=data.get("sheet_name"),
                x_column=data.get("x_column"),
                y_column=data.get("y_column")
            )

        else:

            return jsonify({
                "status": "error",
                "message": "Invalid mode selected."
            }), 400

        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500