import { useEffect, useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

import { Cards } from './Cards';
import { QuestionStore } from './QuestionStore';
import { Rules } from './Rules';


const cardsDummyData = [
	{
		id: 1,
		name: "JJ Birthday!",
		description: "Celebrate JJ birthday",
		difficulty: "Easy",
		pointValue: 10,
	},
	{
		id: 2,
		name: "More Birthday!!!",
		description: "Celebrate HARDER >:o",
		difficulty: "Hard",
		pointValue: 20,
	},
	{
		id: 3,
		name: "Most Bday?",
		description: "Could there be more celebrating???",
		difficulty: "Medium",
		pointValue: 1,
	},
];


function PasswordPrompt({ allTeamsData, setTeamData, setDisplayedPage }) {
	const [enteredPassword, setEnteredPassword] = useState('');
	const [errorIsHidden, setErrorIsHidden] = useState(true);
	return (
		<div>
			<header className="header-holder">
				<p className="site-title">JJ Scavenger Hunt Site :D</p>
			</header>
			<TextField
				id="outlined-basic"
				label="Team Password"
				variant="outlined"
				fullWidth
				value={enteredPassword}
				onChange={(e) => {
					setEnteredPassword(e.target.value);
					if (e.target.value === '') {
						setErrorIsHidden(true);
					}
				}}
			/>
			<p hidden={errorIsHidden} className="error centered">
				Incorrect Password
			</p>
			<br />
			<Button
				style={{ margin: ' 24px auto', fontSize: '18px', background: '#A7E8FE' }}
				className="centered"
				variant="contained"
				disabled={enteredPassword.length < 1}
				onClick={() => {
					allTeamsData.map((team) => {
						if (team.password === enteredPassword) {
							setErrorIsHidden(true);
							setTeamData(team);
							setDisplayedPage('cards');
							return;
						}
					});
					setErrorIsHidden(false);
				}}
			>
				Submit
			</Button>
		</div>
	);
}

export function Welcome({
	displayedPage,
	setDisplayedPage,
}) {
	const [allTeamsData, setAllTeamsData] = useState([{
		teamName: "Team Name",
		points: 69,
		password: 'a',
		favoritedCardIds: [1],
		completedCardIds: [2]
	}]);
	const [teamData, setTeamData] = useState({});
	const [cardsData, setCardsData] = useState(cardsDummyData);
	
	useEffect(() => {
			// call to API gets allTeamsData, then sets it.
		});
	useEffect(() => {
		// call to API gets teamData, then sets it.
		// this is called every 30 seconds?
		// starting when teamData is first updated
	});
	useEffect(() => {
		// call to API to get cardsData. This only happens once?
		// or also happens when they click favorite?
	});
	
	switch(displayedPage) {
		case 'rules':
			return <Rules />;
			break;
		case 'question store':
			return <QuestionStore teamData={teamData} />;
			break;
		case 'cards':
			return <Cards cardsData={cardsData} teamData={teamData} />;
			break;
		default:
			return (
				<PasswordPrompt
					allTeamsData={allTeamsData}
					setDisplayedPage={setDisplayedPage}
					setTeamData={setTeamData}
				/>
			);
			break;
	}
}