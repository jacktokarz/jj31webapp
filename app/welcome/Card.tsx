import { CoinIcon } from './CoinIcon';

export function ChallengeCard({title, value, description}) {
	return (
		<div style={{maxWidth: "300px"}}>
	    <nav className="card-container">
	      <p className="leading-6 text-gray-700 dark:text-gray-200 text-center">
	        {title}
	      </p>
				<div>
					{value}
					{CoinIcon}
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