import React, { useState } from 'react';
import Divider from '@mui/material/Divider';

import { ChallengeCard } from './Card';
import { Filters } from './Filters';
import { type Team } from '../types/Team';
import { WelcomeHeader} from './WelcomeHeader';


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


export function Cards({ cardsData, teamData }) {	
	const originalCards = cardsData.filter((card) => !teamData.completedCardIds.includes(card.id));
	const [displayedCards, setDisplayedCards] = useState([...originalCards]);
	console.log('original: ',originalCards);
	console.log('displayed: ', displayedCards);
	
  return (
    <div>
			<WelcomeHeader
				titleText="JJ's 31st BDAY"
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
  );
}
