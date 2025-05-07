import { useState } from 'react';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import Divider from '@mui/material/Divider';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';


export function Filters({
	filterCards,
	setDisplayedCards,
	originalCards,
	faveCardIds,
}) {
	const [filterInput, setFilterInput] = useState("");
	const [difficultySelection, setDifficultySelection] = useState("");
	const [onlyFavorites, setOnlyFavorites] = useState(false);
	return (
		<div className="filters-container">
			<TextField
				label="Filter"
				value={filterInput}
				onChange={(e) => {
					const newInput = e.target.value;
					setFilterInput(newInput);
					const newDisplay = filterCards(originalCards, faveCardIds, newInput, difficultySelection, onlyFavorites);
					setDisplayedCards(newDisplay);
				}}
				fullWidth
			/>
			<FormControl 
				fullWidth
				sx={{ margin: '12px 0 12px 0' }}
			>
				<InputLabel id="diff-select-label">Filter by Difficulty</InputLabel>
				<Select
		      id="diff-select"
					labelId="diff-select-label"
					value={difficultySelection}
		      onChange={(e) => {
						const diff = e.target.value;
						setDifficultySelection(diff);
						const newDisplay = filterCards(originalCards, faveCardIds, filterInput, diff, onlyFavorites);
						setDisplayedCards(newDisplay);
					}}
		    >
					<MenuItem value={''}>All</MenuItem>
					<MenuItem value={'Easy'}>Easy</MenuItem>
					<MenuItem value={'Medium'}>Medium</MenuItem>
					<MenuItem value={'Hard'}>Hard</MenuItem>
				</Select>
			</FormControl>
			<div className="flex favorites-filter-holder">
				<div
					className="centered half-width"
					onClick={() => {
						setOnlyFavorites(false);
						const newDisplay = filterCards(originalCards, faveCardIds, filterInput, difficultySelection, false);
						setDisplayedCards(newDisplay);
					}}
				>
					<span style={{ textDecoration: onlyFavorites?'none':'underline' }}>Everything</span>
				</div>
				<Divider
					orientation="vertical"
					variant="middle"
					flexItem
				/>
				<div
					className="centered half-width"
					onClick={() => {
						setOnlyFavorites(true);
						const newDisplay = filterCards(originalCards, faveCardIds, filterInput, difficultySelection, true);
						setDisplayedCards(newDisplay);
					}}
				>
					<span style={{ textDecoration: onlyFavorites?'underline':'none' }}>Favorites</span>
				</div>
			</div>
		</div>
	);
}