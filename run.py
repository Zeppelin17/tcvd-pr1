from flask import Flask, request, jsonify
from datetime import datetime
import subprocess


app = Flask(__name__)


@app.route("/api/investingcom", methods=["GET"])
def scrape():
    method = request.args.get("method")
    equity = request.args.get("equity")
    if not method:
        return jsonify({"error": "Missing METHOD parameter"}), 400
    if not equity:
        return jsonify({"error": "Missing EQUITY parameter"}), 400

    try:
        # Es llença el bot passant paràmetres method i equity
        current_datetime = datetime.now().strftime("%Y%m%d%H%M")
        bot_output = f"csv_data/{current_datetime}-{equity}-{method}.csv"

        result = subprocess.run(
            [
                "scrapy",
                "crawl",
                "investingcom_spider",
                "-a",
                f"equity={equity}",
                "-a",
                f"method={method}",
                "-o",
                bot_output,
            ],
            cwd="scraper_bot",
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        with open(f"scraper_bot/{bot_output}", "r") as f:
            data = f.read()

        return jsonify({"data": data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
