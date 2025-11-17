from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Example in-memory data
players = []
tournaments = []

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    player = {
        "name": data.get("name"),
        "uid": data.get("uid"),
        "team": data.get("team"),
        "coins": 0
    }
    players.append(player)
    return jsonify({"message": "Registered successfully", "player": player})

@app.route("/add_tournament", methods=["POST"])
def add_tournament():
    data = request.json
    t = {
        "id": len(tournaments) + 1,
        "name": data.get("name"),
        "date": data.get("date"),
        "fee": data.get("fee"),
        "prize": data.get("prize")
    }
    tournaments.append(t)
    return jsonify({"message": "Tournament added", "tournament": t})

@app.route("/tournaments", methods=["GET"])
def get_tournaments():
    return jsonify(tournaments)

@app.route("/join_tournament", methods=["POST"])
def join_tournament():
    data = request.json
    uid = data.get("uid")
    tournament_id = data.get("tournament_id")

    player = next((p for p in players if p["uid"] == uid), None)
    tournament = next((t for t in tournaments if t["id"] == tournament_id), None)

    if not player or not tournament:
        return jsonify({"error": "Player or tournament not found"}), 400

    if player["coins"] < tournament["fee"]:
        return jsonify({"error": "Not enough coins"}), 400

    player["coins"] -= tournament["fee"]
    return jsonify({"message": f"{player['name']} joined {tournament['name']}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
