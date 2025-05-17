import { useEffect, useState } from 'react';

import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Divider from '@mui/material/Divider';
import TextField from '@mui/material/TextField';

import { WelcomeHeader } from './WelcomeHeader';
import { postQuestion } from './apiCalls';
import { CoinIcon } from './CoinIcon';


function WaitModal({ waitModalOpen, setWaitModalOpen }) {
	return (
		<Modal
		  open={waitModalOpen}
			onClose={() => setWaitModalOpen(false)}
		>
			<div className="basic-modal">
				<p>
					Your question has been successfully submitted.
				</p>
				<p>
					Your <span className="sparkles">JJokens</span> have been <span style={{ textDecoration: 'line-through' }}>foolishly squandered</span> well spent.
				</p>
				<br />
				<p>
					JJ or a JJ stand-in will respond to you in Discord shortly.
				</p>
				<Button
					style={{ margin: ' 24px auto', fontSize: '14px', borderRadius: '8px' }}
					className="centered"
					variant="contained"
					onClick={async () => {
						setWaitModalOpen(false);
					}}
				>
					Close (or you could click outside of this modal to close it. Your choice, man)
				</Button>
			</div>
		</Modal>
	);
}

function ConfirmModal({
	confirmModalData,
	setConfirmModalData,
	teamId,
	setWaitModalOpen,
}) {
	if (confirmModalData === null) {
		return '';
	}
	console.log('confirm modal ', confirmModalData);
	return (
		<Modal
      open={confirmModalData !== null}
			onClose={() => setConfirmModalData(null)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
			<div className="basic-modal">
				<p>
					Are you absolutely <span className="underlined">certain</span> you want to
					spend <span style={{ fontSize: '20px' }}>{confirmModalData.question.cost}</span> hard-earned <span className="sparkles">JJokens</span> to
					ask for the following scoinvenger hint:
				</p>
				<p className="italic">
					{confirmModalData.question.title}
				</p>
				{confirmModalData.input.length > 0
					&& <p style={{ marginTop: '12px'}}>
							With added context:
							<br />
							<span className="italic">{confirmModalData.input}</span>
						</p>
				}
				<Button
					style={{ margin: ' 24px auto', fontSize: '18px', /*background: '#A7E8FE'*/ }}
					className="centered"
					variant="contained"
					onClick={async () => {
						await postQuestion(confirmModalData.question.id, teamId, confirmModalData.input);
						setWaitModalOpen(true);
						setConfirmModalData(null);
					}}
				>
					I COMMIT
				</Button>
			</div>
		</Modal>
	);
}

function QuestionHolder({ teamData, question, setConfirmModalData }) {
	const [questionInput, setQuestionInput] = useState('');
	return (
		<div className="question-holder">
			<div className="question-title">
				{question.title}
			</div>
			<div className="hint-cost">
				{question.cost}
				<CoinIcon />
			</div>
			{question.additional_info === "True"
			&& <TextField
					label="Enter Details"
					value={questionInput}
					onChange={(e) => {
						const newInput = e.target.value;
						setQuestionInput(newInput);
					}}
					fullWidth
				/>
			}
			<Button
				style={{ margin: ' 14px auto', fontSize: '18px' }}
				className="centered"
				variant="contained"
				disabled={
					question.additional_info==="True" && questionInput.length < 1
					||
					question.cost > teamData.points
				}
				onClick={() => {
					setConfirmModalData({ question: question, input: questionInput });
				}}
			>
				Ask
			</Button>
		</div>
	)
}

export function QuestionStore({ teamData, questionsData }) {
	const [confirmModalData, setConfirmModalData] = useState(null);
	const [waitModalOpen, setWaitModalOpen] = useState(false);

	return (
		<div className="full-width">
			<WelcomeHeader
				titleText="Scoinvenger Hints"
				pointValue={teamData.points}
				teamName={teamData.teamName}
			/>
			<Divider
				style={{ marginTop: '80px' }}
				orientation="horizontal"
			/>
			{questionsData.map((question) => (
				<QuestionHolder
					teamData={teamData}
					question={question}
					setConfirmModalData={setConfirmModalData}
				/>
			))}
			<ConfirmModal
				confirmModalData={confirmModalData}
				setConfirmModalData={setConfirmModalData}
				teamId={teamData.id}
				setWaitModalOpen={setWaitModalOpen}
			/>
			<WaitModal
				waitModalOpen={waitModalOpen}
				setWaitModalOpen={setWaitModalOpen}
			/>
		</div>
	);
};