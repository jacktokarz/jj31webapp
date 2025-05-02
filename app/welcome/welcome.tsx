import React from 'react';

import { CoinIcon } from './CoinIcon';
import { ChallengeCard } from './Card';

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


export function Welcome() {
	const cardsData = [
		{
			id: 1,
			name: "JJ Birthday!",
			description: "Celebrate JJ birthday",
			pointValue: 10,
		},
		{
			id: 2,
			name: "More Birthday!!!",
			description: "Celebrate HARDER >:o",
			pointValue: 20,
		},
		{
			id: 3,
			name: "Most Bday?",
			description: "Could there be more celebrating???",
			pointValue: 1,
		},
	];
	const teamData: Team = {
		teamName: "Team Name",
		points: 69,
		favoritedCardIds: [1],
		completedCardIds: [2]
	};
	const displayCards = cardsData.filter((card) => !teamData.completedCardIds.includes(card.id));
  return (
		<main className="centered">
      <div>
				<WelcomeHeader
					pointValue={teamData.points}
					teamName={teamData.teamName}
				/>
				<div>
					{displayCards.map((card) => {
						return (
							<ChallengeCard
								title={card.name}
								value={card.points}
								description={card.description}
							/>
						)
					})}
	      </div>
			</div>
    </main>
  );
}
