'use strict';

let score = 0;
let words = new Set();
let time = 60;

$('#timer').html(time);

$('form').on('submit', handleSubmit);

async function handleSubmit(e) {
	e.preventDefault();
	//creating a variable for our submitted input
	let word = $('input').val();
	word.toLowerCase();
	//if the form is empty then return
	if (!word) return;
	//send this word to the server to check if it is the right response:
	const res = await axios.get('/check-word', { params: { word: word } });
	let response = res.data.response;
	console.log(response);
	$('#response').html(response);
	$('form').trigger('reset');

	if (response == 'ok') {
		if (words.has(word)) {
			return;
		}
		words.add(word);
		score += word.length;
		$('#score').html(`Score: ${score}`);
	}
}

let countDown = setInterval(function() {
	time--;
	$('#timer').html(time);
	stopTimer();
}, 1000);

function stopTimer() {
	if (time < 1) {
		clearInterval(countDown);
		$('form').hide();
		$('.container').append($('<span>').html('GAME OVER!!'));
		endGame();
	}
}

async function endGame() {
	await axios.post('/end-game', { score: score });
}

let game=new BoggleGame();
