import questions from '../data/QuestionsDb.json';
import { useEffect, useState } from "react";
import { useHistory } from 'react-router-dom';
 
const QuizQuestions = () => {
    const [num, setNum] = useState(1);
    const [question, setQuestion] = useState(null);
    const [options, setOptions] = useState(null);
    const [choices, setChoices] = useState({});

    const maxNum = questions.questions.length;
    const history = useHistory(); 
    
    useEffect(() => {
        const getQuestion = questions.questions.find((question) => question.id === num);
        setQuestion(getQuestion.question);
        setOptions(getQuestion.options);    
    }, [num])

    const handleButtons = (state) => {
        if (state === 'back') {
            setNum(Math.max(1, num - 1));
        } else if (state === 'next') {
            setNum(Math.min(maxNum, num + 1));
        } else if (state === 'submit') {
            if (Object.keys(choices).length === maxNum) {
                history.push('/quiz/result');
            } else {
                alert('Please answer all questions before submitting.');
            }
        }   
    }

    const handleOptionClick = (opt) => {
        setChoices({
          ...choices,
          [num]: opt
        });
      }

    return (
        <div className="quiz-questions">
            <div className="quiz-page">
                <div className="question-headline">Question {num}</div>
                <div className="bar-1"/>
                <div className="question-bar">{ question }</div> 
                <div className="question-options">
                    {options && options.map((opt, index) => (
                        <div
                            key={index}
                            className={`option-box ${choices[num] === index ? 'selected' : ''}`}
                            onClick={() => handleOptionClick(index)}
                        >
                            { opt }
                        </div>
                    ))}
                </div>           
                <div className="button-container">
                    <button className='button-1' onClick={() => handleButtons('back')}>Back</button>
                    { num === maxNum && (
                        <button className='button-2' onClick={() => handleButtons('submit')}>Submit</button>
                    )}
                    { num !== maxNum && (
                        <button className='button-3' onClick={() => handleButtons('next')}>Next</button>
                    )}
                </div>  
                <div className="foot-note"> { num } of { maxNum } Questions</div>        
            </div>
        </div>
    );
}


export default QuizQuestions;

