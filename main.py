{% extends 'base.html' %}
{% block meta %}
<title>Sports Logo Guessing Game | NFL</title>
<meta name="description" content="Try your hand at guessing the names of various team logos. See if you can score more than your friends and family.">


{% endblock %}
{% block content %}
<style>
    body {
        background-color: #3f9b0b;
        background-image: url("{{ url_for('static', filename='images/football-no-lines.png') }}");
        background-repeat: repeat;
        background-size: auto;
    }
</style>

<div class="container mt-5">
    <div class="row justify-content-md-center">
        <div class="bg-white p-3 rounded shadow-sm mb-2 col-md-6">
            <h1 class="text-center">Guess the Sports Logo</h1>
        </div>
    </div>

    <!-- Game mode buttons with tooltips -->
  <div class="d-flex justify-content-center mt-3">
    <select id="league-filter" class="form-select me-2" style="max-width: 200px;">
        <option disabled selected>Select a league</option>

        <optgroup label="American Football">
            <option value="NFL" selected>NFL</option>
            <option value="UFL">UFL</option>
        </optgroup>

        <optgroup label="Basketball">
            <option value="NBA">NBA</option>
            <option value="WNBA">WNBA</option>
            <option value="NBA G League">NBA G League</option>
        </optgroup>

        <optgroup label="Ice Hockey">
            <option value="NHL">NHL</option>
            <option value="AHL">AHL</option>
        </optgroup>

            <!-- Add other leagues as options -->
    </select>
        <button id="start-game" class="btn btn-primary me-2" data-bs-toggle="tooltip" title="Start a timed game with 30 seconds on the clock!">Start Timed Game</button>
        <button id="free-play" class="btn btn-info" data-bs-toggle="tooltip" title="Play without time limits and guess at your own pace!">Free Play</button>
    </div>


    <!-- Timer and score display -->
    <div class="d-flex justify-content-center m-3">
        <h3 id="timer" class="text-white mx-1"></h3>
        <h3 id="score" class="text-white mx-1">Score: 0</h3>
    </div>

    <!-- Card for the logo -->
    <div class="card mx-auto mt-3" style="max-width: 300px; height: 300px; background-color: #f8f9fa; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); display: none;">
        <div class="card-body d-flex justify-content-center">
            <img id="team-logo" src="" alt="Team Logo" class="img-fluid rounded" style="max-width: 300px; min-width: 200px; max-height: 300px; min-height: 200px;">
        </div>
    </div>

    <!-- Guess input and buttons -->
    <div class="d-flex justify-content-center mt-3" style="display: none;">
        <input type="text" id="team-guess" class="form-control me-2" placeholder="Type your guess here..." style="max-width: 300px;">
    </div>
    <div class="d-flex justify-content-center mt-2" style="display: none;">
        <button id="submit-guess-btn" class="btn btn-primary me-2" onclick="submitGuess()" disabled>Submit Guess</button>
        <button class="btn btn-secondary" onclick="skipTeam()">Skip</button>
    </div>

    <div id="result-message" class="alert d-none mt-3 mx-auto" style="max-width: 600px;" role="alert"></div> <!-- Bootstrap alert -->

        <!-- Modal for sharing score -->
    <div class="modal fade" id="shareScoreModal" tabindex="-1" aria-labelledby="shareScoreModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="shareScoreModalLabel">Game Over!</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p id="final-score-message">Your score is: 0</p>
                    <p>Share your score with your friends!</p>
                    <div class="input-group mb-3">
                        <input type="text" id="share-url" class="form-control" value="{{ request.scheme }}://{{ request.host }}{{ request.path }}" readonly>
                    </div>
                    <button class="btn btn-outline-secondary" onclick="copyToClipboard()">Copy Link</button>
                    <a id="twitter-share" href="#" target="_blank" class="btn btn-info">Share on <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-twitter-x" viewBox="0 0 16 16">
                            <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z"/>
                        </svg></a>
                    <a id="facebook-share" href="#" target="_blank" class="btn btn-primary">Share on <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                            <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/>
                        </svg></a>
                </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // Initialize Bootstrap tooltips
    document.addEventListener('DOMContentLoaded', function () {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    });

    let currentTeam = '';
    let currentMonikers = [];
    let lastGuess = '';
    let score = 0;
    let usedTeams = new Set();
    let timerInterval;
    let timeLeft = 30; // 30 seconds countdown
    let isFreePlay = false; // Track if the user is in Free Play mode

    document.getElementById('start-game').addEventListener('click', startTimedGame);
    document.getElementById('free-play').addEventListener('click', startFreePlay);

    function startTimedGame() {
        isFreePlay = false;
        score = 0;
        clearInterval(timerInterval)
        timeLeft = 30;
        usedTeams.clear();
        document.getElementById('score').textContent = 'Score: 0';
        document.getElementById('timer').textContent = `Time Left: ${timeLeft}s`;

        // Show the game elements
        showGameElements();

        loadNewLogo(); // Load the first logo
        startTimer();
    }

    function startFreePlay() {
        if (timerInterval) {
            clearInterval(timerInterval); // Stop the timer if it's running
            timerInterval = null; // Reset the timer interval variable
        }

        isFreePlay = true;
        score = 0;
        usedTeams.clear();
        document.getElementById('score').textContent = 'Score: 0';
        document.getElementById('timer').textContent = ''; // Hide timer in Free Play mode

        // Show the game elements
        showGameElements();

        loadNewLogo(); // Load the first logo without starting the timer
    }

    function showGameElements() {
        document.querySelector('.card').style.display = 'block';
        document.querySelector('.d-flex.mt-3:nth-of-type(2)').style.display = 'flex';
        document.querySelector('.d-flex.mt-2').style.display = 'flex';
    }

    function startTimer() {
        timerInterval = setInterval(() => {
            timeLeft--;
            document.getElementById('timer').textContent = `Time Left: ${timeLeft}s`;

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                endGame();
            }
        }, 1000);
    }

        function endGame() {
            document.getElementById('result-message').classList.remove('d-none', 'alert-success', 'alert-danger');
            document.getElementById('result-message').classList.add('alert-info');
            document.getElementById('result-message').textContent = `Time's up! Your final score is: ${score}`;

            hideGameElements();

            // Update the modal with the final score
            document.getElementById('final-score-message').textContent = `Your score is: ${score}`;

            // Generate the Twitter share link
            const tweetText = `I scored ${score} points guessing sports logos! Can you beat my score?`;
            const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}&url=${encodeURIComponent(window.location.href)}`;
            document.getElementById('twitter-share').href = tweetUrl;

            // Generate the Facebook share link
            const facebookShareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}&quote=${encodeURIComponent("I scored " + score + " points guessing sports logos! Can you beat my score?")}`;
            document.getElementById('facebook-share').href = facebookShareUrl;

            // Show the share modal
            const shareModal = new bootstrap.Modal(document.getElementById('shareScoreModal'));
            shareModal.show();
        }

        function hideGameElements() {
            document.querySelector('.card').style.display = 'none';
            document.querySelector('.d-flex.mt-3:nth-of-type(2)').style.display = 'none';
            document.querySelector('.d-flex.mt-2').style.display = 'none';
        }

        function copyToClipboard() {
            const shareUrlInput = document.getElementById('share-url');
            shareUrlInput.select();
            document.execCommand('copy');
            alert('Link copied to clipboard!');
        }

    document.getElementById('league-filter').addEventListener('change', loadNewLogo);

    function loadNewLogo() {
        const selectedLeague = document.getElementById('league-filter').value;

        fetch(`/get_logo?league=${selectedLeague}`)
            .then(response => {
                if (!response.ok) throw new Error('No teams available for this league');
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    alert(data.error);  // Optional: display an alert if no teams are available
                    return;
                }

                if (usedTeams.has(data.team)) {
                    loadNewLogo();
                    return;
                }

                document.getElementById('team-logo').src = data.image;
                currentMonikers = data.moniker;
                currentTeam = data.team;
                document.getElementById('team-guess').value = '';
                document.getElementById('result-message').classList.add('d-none');
                lastGuess = '';

                usedTeams.add(data.team);
                document.getElementById('submit-guess-btn').disabled = false; // Enable the Submit Guess button
            })
            .catch(error => console.error('Error:', error));
    }


    function submitGuess() {
        const guess = document.getElementById('team-guess').value;
        lastGuess = guess;
        document.getElementById('submit-guess-btn').disabled = true;

        fetch('/check_guess', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ guess: guess, team: currentTeam, moniker: currentMonikers })
        })
        .then(response => response.json())
        .then(data => {
            const resultMessage = document.getElementById('result-message');
            resultMessage.classList.remove('d-none');

            if (data.result === 'correct') {
                resultMessage.classList.remove('alert-danger');
                resultMessage.classList.add('alert-success');
                resultMessage.textContent = 'Correct!';
                score++;
                document.getElementById('score').textContent = `Score: ${score}`;
                setTimeout(loadNewLogo, 1000);
            } else {
                resultMessage.classList.remove('alert-success');
                resultMessage.classList.add('alert-danger');
                resultMessage.textContent = `Your previous guess was: "${lastGuess}". Please try again!`;
                document.getElementById('team-guess').value = '';
                document.getElementById('submit-guess-btn').disabled = false;
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function skipTeam() {
        document.getElementById('submit-guess-btn').disabled = true;
        const resultMessage = document.getElementById('result-message');
        resultMessage.classList.remove('d-none', 'alert-success', 'alert-danger');
        resultMessage.classList.add('alert-info');
        resultMessage.textContent = `The previous answer was: ${currentTeam}`;
        setTimeout(loadNewLogo, 2000);
    }

    document.getElementById('team-guess').addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            submitGuess();
        }
    });
</script>
{% endblock %}
