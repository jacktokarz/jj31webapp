import { CoinIcon } from './CoinIcon';

export function WelcomeHeader({titleText, pointValue, teamName}) {
	return (
		<header className="header-holder">
			<p className="site-title">{titleText}</p>
			<div className="gray-line" />
			<div className="inline vertical-align">
				<div className="inline">{teamName}</div>
				<div className="inline float-right">
					{pointValue}
					<CoinIcon />
				</div>
			</div>
		</header>
	);
};