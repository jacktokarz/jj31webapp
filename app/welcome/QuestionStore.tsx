import { WelcomeHeader } from './WelcomeHeader';

export function QuestionStore({ teamPointValue, teamName }) {
	return (
		<div>
			<WelcomeHeader
				titleText="Question Store"
				pointValue={teamPointValue}
				teamName={teamName}
			/>
		</div>
	);
};