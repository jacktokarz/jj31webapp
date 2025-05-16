import { useEffect, useState } from 'react';
import { useCookies } from 'react-cookie';

import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

import { Cards } from './Cards';
import { QuestionStore } from './QuestionStore';
import { Rules } from './Rules';
import { getCards, getTeams, getTeamData } from './apiCalls';



function PasswordPrompt({ allTeamsData, setTeamData, setDisplayedPage, setCookie }) {
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
							setCookie('loggedInUser', team);
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
	const [cookies, setCookie] = useCookies<'loggedInUser', CookieValues>(['loggedInUser']);
	const [allTeamsData, setAllTeamsData] = useState([]);
	const [teamData, setTeamData] = useState(cookies.loggedInUser);
	const [cardsData, setCardsData] = useState([]);
	const [questionsData, setQuestionsData] = useState([]);
	
	useEffect(() => {
			async function callGetAllData() {
				const newCards = await getCards();
				console.log('setting cardsData to: ',newCards);
				setCardsData(newCards);
				if (loggedInUser !== null) {
					const newTeam = await getTeamData(loggedInUser.id);
					console.log('setting teamData to: ', newTeam);
					setTeamData(newTeam);
				}
			}
			callGetAllData();
			setInterval(function(){
				callGetAllData();
			}, 30000)
		}, []);
	useEffect(() => {
		async function callGetDataOnce() {
			const newTeams = await getTeams();
			console.log('setting teamsData to: ', newTeams);
			setAllTeamsData(newTeams);
			const newQuestions = await getQuestions();
			console.log('setting questionsData to: ', newQuestions);
			setQuestionsData(newQuestions);
		}
		callGetDataOnce();
	}, []);
	
	switch(displayedPage) {
		case 'rules':
			return <Rules />;
			break;
		case 'question store':
			return <QuestionStore teamData={teamData} questionsData={questionsData} />;
			break;
		case 'cards':
			return <Cards cardsData={cardsData} teamData={teamData} />;
			break;
		default:
			return (
				<PasswordPrompt
					setCookie={setCookie}
					allTeamsData={allTeamsData}
					setDisplayedPage={setDisplayedPage}
					setTeamData={setTeamData}
				/>
			);
			break;
	}
}