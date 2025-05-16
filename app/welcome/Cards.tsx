import React, { useState } from 'react';
import Divider from '@mui/material/Divider';

import { ChallengeCard } from './Card';
import { Filters } from './Filters';
import { type Team } from '../types/Team';
import { WelcomeHeader} from './WelcomeHeader';


export function Cards({ cardsData, teamData, setTeamData }) {
	const originalCards = cardsData.filter((card) => !teamData.completed_cards.includes(card.id));
	const [displayedCards, setDisplayedCards] = useState([...originalCards]);
	
  return (
    <div className="full-width">
			<WelcomeHeader
				titleText="Challenge Cards"
				pointValue={teamData.points}
				teamName={teamData.name}
			/>
			<Filters
				setDisplayedCards={setDisplayedCards}
				originalCards={originalCards}
				faveCardIds={teamData.favorite_cards}
			/>
			<Divider
				orientation="horizontal"
			/>
			<div>
				{displayedCards.map((card) => {
					return (
						<ChallengeCard
							key={card.id}
							teamData={teamData}
							setTeamData={setTeamData}
							card={card}
						/>
					)
				})}
      </div>
		</div>
  );
}
