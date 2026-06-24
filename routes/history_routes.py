import json

from flask import Blueprint, jsonify

history_bp = Blueprint("history_bp", __name__)

HISTORY_FILE = "history/analysis_history.json"


@history_bp.route("/history", methods=["GET"])
def get_history():

    try:

        with open(HISTORY_FILE, "r") as file:

            history = json.load(file)

        return jsonify({
            "status": "success",
            "data": history
        })

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500