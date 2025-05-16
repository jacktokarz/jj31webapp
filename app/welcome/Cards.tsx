import React, { useState } from 'react';
import Divider from '@mui/material/Divider';

import { ChallengeCard } from './Card';
import { Filters } from './Filters';
import { type Team } from '../types/Team';
import { WelcomeHeader} from './WelcomeHeader';


function updateFavorites(id) {
	console.log("send API call to update team's favorites list with ",id);
	console.log("temporarily update local version of team data to uinclude or not include this id");
}


export function Cards({ cardsData, teamData }) {	
	const originalCards = cardsData.filter((card) => !teamData.completedCardIds.includes(card.id));
	const [displayedCards, setDisplayedCards] = useState([...originalCards]);
	
  return (
    <div>
			<WelcomeHeader
				titleText="JJ's 31st BDAY"
				pointValue={teamData.points}
				teamName={teamData.teamName}
			/>
			<Filters
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
							title={card.title}
							difficulty={card.difficulty}
							value={card.value}
							description={card.description}
						/>
					)
				})}
      </div>
		</div>
  );
}
