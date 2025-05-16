const apiBase = 'http://127.0.0.1:8000';

async function callApi(argument) {
	const response = await fetch(`${apiBase}/${argument}/`);
	const jsonResponse = response.json();
	return jsonResponse;
}

export async function getCards() {
	const allCards = await callApi('cards');
	return allCards;
}

export async function postFavorite() {
	// adds a card id to the team's favorite list
}

export async function getTeams() {
	const allTeams = await callApi('teams');
	return allTeams;
}

export async function getTeamData(id) {
	const teamData = await callApi(`teams/${id}`);
	return teamData;
}

export async function getQuestions() {
	const allQuestions = await callApi('questions');
	return allQuestions;
}

export async function postQuestion() {
	console.log('posting....');
}