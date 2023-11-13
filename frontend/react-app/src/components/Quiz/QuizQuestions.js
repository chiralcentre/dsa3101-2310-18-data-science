//import questions from '../data/QuestionsDb.json';
import { useEffect, useState } from "react";
import useFetch from "./useFetch";
import QuizResult from "./QuizResult";
 
const QuizQuestions = () => {
    const [num, setNum] = useState(1);
    const [question, setQuestion] = useState(null);
    const [options, setOptions] = useState(null);
    const [choices, setChoices] = useState({});
    const [modalVisible, setModalVisible] = useState(false);
    const [questions, setQuestions] = useState({ questions: [] }); 
    const maxNum = questions.questions.length; 
    const choicesLength = Object.keys(choices).length;

    const data = useFetch('http://localhost:5000/quiz-questions');
    const transformData = (data) => {
        const parsedData = JSON.parse(data);
        const transformed = {
            questions: parsedData.map((item, index) => ({
                question: item.question,
                options: [
                    item.A.toString(),
                    item.B.toString(),
                    item.C.toString(),
                    item.D.toString()
                ],
                id: index + 1,
            })),
        };
        setQuestions(transformed);
    }

    useEffect(() => {
        if (data) {
            transformData(data);
        }
    }, [data]); 
    
    useEffect(() => {
        if (questions && questions.questions) {
            const getQuestion = questions.questions.find((question) => question.id === num);
            if (getQuestion) {
                setQuestion(getQuestion.question);
                setOptions(getQuestion.options);
            }
        }
    }, [num, questions]);    

    const handleButtons = (state) => {
        if (state === 'back') {
            setNum(Math.max(1, num - 1));
        } else if (state === 'next') {
            setNum(Math.min(maxNum, num + 1));
        } else if (state === 'submit') {
            setModalVisible(true);
        } else if (state === 'closeModal') {
            setModalVisible(false);
        } else if (state === 'success') {
            setSwap(true);
        }
    }

    const handleOptionClick = (opt, isChoiceAvailable) => {
        if (isChoiceAvailable) {
            const { [num]: removedChoice, ...updatedChoices } = choices;
            setChoices(updatedChoices);
        } else {
            setChoices({
              ...choices,
              [num]: opt
            });
        }
    }

    const [swap, setSwap] = useState(false);

    return (
        <div className="quiz-questions">
            {!swap && (
                <div className="quiz-page">
                    <div className="question-headline">
                        <p>Question {num}</p>
                        <div className="number-note"> { num } of { maxNum } Questions</div>       
                    </div>    
                    <div className="bar-1"/>
                    <div className="question-bar">{ question }</div> 
                    <div className="question-options">
                        {options && options.map((opt, index) => {
                            const isChoiceAvailable = choices[num] === index;
                            return (
                                <div
                                    key={ index }
                                    className={`option-box ${choices[num] === index ? 'selected' : ''}`}
                                    onClick={() => handleOptionClick(index, isChoiceAvailable)}
                                >
                                    { opt }
                                </div>
                            );
                        })}
                    </div>  
                    <div className="button-quiz-container">
                        <button className='button-quiz-1' onClick={() => handleButtons('back')}>Back</button>
                        {num === maxNum && (
                            <button className='button-quiz-2' onClick={() => handleButtons('submit')}>Submit</button>
                        )}
                        {num !== maxNum && (
                            <button className='button-quiz-3' onClick={() => handleButtons('next')}>Next</button>
                        )}
                    </div>                    
                    {modalVisible && (
                        choicesLength === maxNum ? (
                            <div className="modal">
                                <div className="modal-container">
                                    <img src="/img/Checklist.png" alt="" className='modal-img'/>
                                    <p>Your respond has been<br />submitted.</p>
                                    <button className='button-quiz-5' onClick={() => handleButtons('success')}>See your result!</button>
                                </div>
                            </div>
                        ) : (
                            <div className="modal">
                                <div className="modal-container">
                                    <img src="/img/Alert.png" alt="" className='modal-img'/>
                                    <p>Please answer all questions<br />before submitting.</p>
                                    <button className='button-quiz-4' onClick={() => handleButtons('closeModal')}>Back</button>
                                </div>
                            </div>
                        )
                    )}
                </div>
            )}
            {swap && <QuizResult choices={choices} />}
        </div>
    );
}

export default QuizQuestions;

