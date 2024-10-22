from flask import Flask, render_template, request, redirect, url_for, jsonify
from urllib.parse import quote as url_quote
import requests, json
from sports_teams import football_teams
import random

app = Flask(__name__)


@app.route('/logo_guessing_game')
def logo_guessing_game():
    return render_template('logo_guessing_game.html')

@app.route('/get_logo', methods=['GET'])
def get_logo():
    team = random.choice(football_teams)
    return jsonify({"image": team["logo"], "team": team["team"], "moniker": team["moniker"]})

@app.route('/check_guess', methods=['POST'])
def check_guess():
    data = request.json
    team_guess = data.get('guess', '').strip().lower()
    correct_team = data.get('team', '').strip().lower()
    monikers = [moniker.strip().lower() for moniker in data.get('moniker', [])]

    # Check if the guess matches the team name or any of the monikers
    if team_guess == correct_team or team_guess in monikers:
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "incorrect"})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
