import React, { useState } from 'react';
import Divider from '@mui/material/Divider';

import { CoinIcon } from './CoinIcon';
import { ChallengeCard } from './Card';
import { Filters } from './Filters';
import { type Team } from '../types/Team';

function WelcomeHeader({pointValue, teamName}) {
	return (
		<header className="header-holder">
			<p className="site-title">JJ's 31st BDAY</p>
			<div className="gray-line" />
			<div className="inline">
				<div className="inline">{teamName}</div>
				<div className="inline float-right">
					{pointValue}
					<CoinIcon />
				</div>
			</div>
		</header>
	);
};

/*
function CardsDisplay({hiddenCardIds}) {
	return(
		<div>
			{}
			<ChallengeCard
				title=
				value={10}
				description=
			/>
		</div>
	);
};
*/

const cardsData = [
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

function filterCards(
	originalCards,
	faveCardIds,
	filterText,
	filterDiff,
	onlyFavorites,
) {
	let newCards = [...originalCards];
	console.log('filtering with: ',filterText, filterDiff, onlyFavorites, faveCardIds);
	if (onlyFavorites) {
		newCards = newCards.filter(card => {console.log('id', card.id); return faveCardIds.includes(card.id)});
	}
	if (filterDiff !== '') {
		newCards = newCards.filter(card => (card.difficulty === filterDiff));
	}
	if (filterText.length > 2) {
		newCards = newCards.filter(card => (card.name.includes(filterText) || card.description.includes(filterText)));
	}
	return newCards;
}

function updateFavorites(id) {
	console.log("send API call to update team's favorites list with ",id);
	console.log("temporarily update local version of team data to uinclude or not include this id");
}


export function Welcome() {
	const teamData: Team = {
		teamName: "Team Name",
		points: 69,
		favoritedCardIds: [1],
		completedCardIds: [2]
	};
	const originalCards = cardsData.filter((card) => !teamData.completedCardIds.includes(card.id));
	const [displayedCards, setDisplayedCards] = useState([...originalCards]);
	console.log('original: ',originalCards);
	console.log('displayed: ', displayedCards);
	
  return (
		<main className="centered">
      <div>
				<WelcomeHeader
					pointValue={teamData.points}
					teamName={teamData.teamName}
				/>
				<Filters
					filterCards={filterCards}
					setDisplayedCards={setDisplayedCards}
					originalCards={originalCards}
					faveCardIds={teamData.favoritedCardIds}
				/>
				<Divider
					orientation="horizontal"
				/>
				<div>
					{displayedCards.map((card) => {
						return (
							<ChallengeCard
								key={card.id}
								faveCardIds={teamData.favoritedCardIds}
								updateFavorites={updateFavorites}
								id={card.id}
								title={card.name}
								difficulty={card.difficulty}
								pointValue={card.pointValue}
								description={card.description}
							/>
						)
					})}
	      </div>
			</div>
    </main>
  );
}
