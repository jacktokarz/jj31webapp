import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCoins } from '@fortawesome/free-solid-svg-icons';

const coinIcon = <FontAwesomeIcon icon={faCoins} />;

function ChallengeCard({title, value, description}) {
	return (
		<div className="max-w-[300px] w-full space-y-6 px-4">
	    <nav className="rounded-3xl border border-gray-200 p-6 dark:border-gray-700 space-y-4">
	      <p className="leading-6 text-gray-700 dark:text-gray-200 text-center">
	        {title}
	      </p>
				<div>
					{value}
					{coinIcon}
				</div>
				<p>
					Requirements:
					<br />
					{description}
				</p>
	    </nav>
	  </div>
	);
}

export function Welcome() {
	const teamName = "Team Name";
	const pointValue = 69;
  return (
    <main className="flex items-center justify-center pt-16 pb-4">
      <div className="flex-1 flex flex-col items-center gap-16 min-h-0">
        <header className="flex flex-col items-center gap-9">
					<div>
						<h2>{teamName}</h2>
						<p>
							{pointValue}
							{coinIcon}
						</p>
					</div>
					<ChallengeCard
						title="JJ's Birthday!"
						value={10}
						description="Celebrate JJ's birthday"
					/>
					<ChallengeCard
						title="More Birthday!!!"
						value={20}
						description="Celebrate HARDER >:o"
					/>
        </header>
      </div>
    </main>
  );
}
