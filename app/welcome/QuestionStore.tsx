import { WelcomeHeader } from './WelcomeHeader';

export function QuestionStore({ teamData }) {
	return (
		<div>
			<WelcomeHeader
				titleText="Question Store"
				pointValue={teamData.points}
				teamName={teamData.teamName}
			/>
		</div>
	);
};