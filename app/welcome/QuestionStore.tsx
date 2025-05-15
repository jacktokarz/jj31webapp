import { useEffect, useState } from 'react';

import Button from '@mui/material/Button';
import Modal from '@mui/material/Modal';
import Divider from '@mui/material/Divider';

import { WelcomeHeader } from './WelcomeHeader';
import { getQuestions, postQuestion } from './apiCalls';

const fakeQuestions = [
	{
		title: 'Where is JJ?',
		cost: 100,
		requiresInput: true,
	}
];

function WaitModal({ waitModalOpen, setWaitModalOpen }) {
	return (
		<Modal
		  open={waitModalOpen}
			onClose={setWaitModalOpen(false)}
		>
			<p>
				Your question has been successfully submitted.
			</p>
			<p>
				Your JJokens have been <span>foolishly squandered</span> well spent.
			</p>
			<p>
				JJ or a JJ stand-in will respond to you in Discord shortly.
			</p>
			<Button
				style={{ margin: ' 24px auto', fontSize: '18px', background: '#A7E8FE' }}
				className="centered"
				variant="contained"
				onClick={async () => {
					setWaitModalOpen(false);
				}}
			>
				Close (or you could click outside of this modal to close it. Your choice, man)
			</Button>
		</Modal>
	);
}

function ConfirmModal({
	confirmModalData,
	setConfirmModalData,
	teamName,
	setWaitModalOpen,
}) {
	return (
		<Modal
      open={comfirmModalData !== null}
			onClose={() => setConfirmModalData(null)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
			<p>
				Are you absolutely certain you want to spend {confirmModalData.question.cost} hard-earned JJ bucks to ask for the following <span className="sparkles">scoinvenger hint</span>:
			</p>
			<p>
				{confirmModalData.question}
			</p>
			{confirmModalData.input !== null
				&& <p>
						With added context: {confirmModalData.input}
					</p>
			}
			<Button
				style={{ margin: ' 24px auto', fontSize: '18px', background: '#A7E8FE' }}
				className="centered"
				variant="contained"
				onClick={async () => {
					await postQuestion(teamName, confirmModalData.question);
					setConfirmModalData(null);
				}}
			>
				I COMMIT
			</Button>
		</Modal>
	);
}

function QuestionHolder({ question }) {
	const [questionInput, setQuestionInput] = useState('');
	
	return (
		<div className="question-holder">
			<div className="question-title">
				{question.title}
			</div>
			{question.requiresInput
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
				style={{ margin: ' 24px auto', fontSize: '18px', background: '#A7E8FE' }}
				className="centered"
				variant="contained"
				disabled={question.requiresInput && questionInput.length < 1}
				onClick={() => {
					setConfirmModalData({ question: question, input: questionInput });
				}}
			>
				Ask
			</Button>
		</div>
	)
}

export function QuestionStore({ teamData }) {
	const [questions, setQuestions] = useState([]);
	const [confirmModalData, setConfirmModalData] = useState(null);
	const [waitModalOpen, setWaitModalOpen] = useState(false);
	
	useEffect(() => {
		// this is called every... 30 seconds?
		async function callGetQuestions() {
			const questionList = await getQuestions();
			if (Array.isArray(questionList)) {
				setQuestions(questionList);							
			}
		};
		callGetQuestions();
	}, []);
	
	return (
		<div>
			<WelcomeHeader
				titleText="Scoinvenger Hints"
				pointValue={teamData.points}
				teamName={teamData.teamName}
			/>
			<Divider
				orientation="horizontal"
			/>
			{questions.map((question) => {
				<QuestionHolder
					question={question}
				/>
			})}
			<ConfirmModal
				confirmModalData={confirmModalData}
				setConfirmModalData={setConfirmModalData}
				teamName={teamData.name}
				setWaitModalOpen={setWaitModalOpen}
			/>
			<WaitModal
				waitModalOpen={waitModalOpen}
				setWaitModalOpen={setWaitModalOpen}
			/>
		</div>
	);
};