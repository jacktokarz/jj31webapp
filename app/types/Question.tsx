export type Question {
	id: string,
	title: string,
	description: string,
	cost: number,
	category: Enumerator,
	needsAdditionalInfo: boolean,
}