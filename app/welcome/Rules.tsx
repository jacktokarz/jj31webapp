import Divider from '@mui/material/Divider';

export function Rules() {
	return (
		<div className="full-width">
			<p className="site-title">Rules</p>
			<Divider
				style={{ margin: '12px' }}
				orientation="horizontal"
			/>
			<div className="subtitle">
				The goal is simple: Get the most points.
			</div>​​
			<ol style={{ marginLeft: "16px" }}>
				<li>
					You get points by completing cards.
				</li>
				<li>
					The harder the card, the more points you get. However, you can get the most points by physically finding me in New York City.
				</li>
				<li>
					The cards for finding me are labelled "Hide and Seek" (try using the Filter to find them).
				</li>
				<li>
					For hints on where to find me, you can spend your points (aka JJokens) on the Scoinvenger Hints page.
				</li>
				<li>
					Whatever team finds me in the shortest time will get a large amount of points!
				</li>
				<li>
					With every task y’all will have to submit proof that you were there with a selfie in your discord chat.
				</li>	
				<li>
					Check the Discord group for announcements and to chat c:
				</li>
			</ol>
			<br />
			<div className="subtitle">
				Where can I hide?
			</div>
			<ul>​
				<li>
					I'll hide once every 2.5 hours (11, 1:30, shorter round of 4-6)
				</li>
				<li>
					I'll never be further than 10 minutes from a train station
				</li>
				<li>
					I will also give which borough I'm in at the very start of each round
				</li>
			</ul>
		</div>
	);
};