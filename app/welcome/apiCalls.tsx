const apiBase = 'http://127.0.0.1:8000';

async function callApi(argument) {
	const response = await fetch(`${apiBase}/${argument}/`);
	const jsonResponse = response.json();
	return jsonResponse;
}

async function postApi(argument, body) {
	const response = await fetch(`${apiBase}/${argument}/`,
		{
		  method: "POST",
			headers: {
	      'Accept': 'application/json',
	      'Content-Type': 'application/json'
	    },
		  body: JSON.stringify(body),
		}
	);
	const jsonResponse = response.json();
	return response;
}

export async function getCards() {
	const allCards = await callApi('cards');
	return allCards;
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

export async function postFavorite(cardId, teamId) {
	const response = await postApi(`cards/${cardId}/favorite`, { team_id: teamId });
}

export async function postUnfavorite(cardId, teamId) {
	const response = await postApi(`cards/${cardId}/unfavorite`, { team_id: teamId });
}

export async function postQuestion(questionId, teamId) {
	const response = await postApi(`questions/${questionId}`, { team_id: teamId });
}