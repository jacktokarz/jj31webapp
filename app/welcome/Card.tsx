import { useState } from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Icon from '@mui/material/Icon';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import Divider from '@mui/material/Divider';

import { CoinIcon } from './CoinIcon';

export function ChallengeCard({
	faveCardIds,
	updateFavorites,
	id,
	title,
	difficulty,
	value,
	description,
}) {
	const [expanded, setExpanded] = useState<string | false>('panel1');
	
	const handleChange = (panel: string) => (event: React.SyntheticEvent, newExpanded: boolean) => {
		setExpanded(newExpanded ? panel : false);
	};
	
	return (
		<div className="card-container">
			<Accordion
				style={{
					boxShadow: '6px 6px 10px #A7E8FE, -3px -3px 6px #DD4B60',
					borderRadius: '18px',
				}}
				expanded={expanded === title}
				onChange={handleChange(title)}
			>
        <AccordionSummary
					className="card-title"
					expandIcon={<ExpandMoreIcon />}
				>
					{title}
        </AccordionSummary>
        <AccordionDetails>
					<Divider style={{margin: '-16px 0 16px 0'}} />
					<div className="card-details">
						<div
							className={`difficulty-label difficulty-${difficulty}`}
						>
							{difficulty}
						</div>
						<div>
							{value}
							<CoinIcon />
							{faveCardIds.includes(id)
								? <StarIcon onClick={() => updateFavorites(id)} className="absolute-right" />
								: <StarBorderIcon onClick={() => updateFavorites(id)} className="absolute-right" />
							}
							
						</div>
					</div>
					<p>
						{description}
					</p>
				</AccordionDetails>
			</Accordion>
	  </div>
	);
}