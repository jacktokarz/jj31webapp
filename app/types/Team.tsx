export type Team = {
	id: string,
	name: string,
	memberNames: Array<string>,
	points: number,
	password: string,
	completedCardIds: Array<string>,
	favoriteCardIds: Array<string>,
	askedQuestionIds: Array<string>,
};