import questions from './data/QuestionsDb.json';
import { useEffect, useState } from "react";
import { useHistory } from 'react-router-dom';
 
const QuizQuestions = () => {
    const [num, setNum] = useState(1);
    const [question, setQuestion] = useState(null);
    const [options, setOptions] = useState(null);
    const [choices, setChoices] = useState({});

    const maxNum = questions.questions.length;
    const currentChoice = choices[num];
    const history = useHistory(); 
    
    useEffect(() => {
        const getQuestion = questions.questions.find((question) => question.id === num);
        setQuestion(getQuestion.question);
        setOptions(getQuestion.options);    
    }, [num])

    const handleButtons = (state) => {
        if (state === 'back') {
            setNum(Math.max(1, num - 1));
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

        setNum(Math.min(maxNum, num + 1));
      }
    
    //question && console.log(question)
    //options && console.log(options)

    

    return (
        <div className="quiz-questions">
            <h1>Question {num}</h1>
            <h2>{question}</h2>
            {options && options.map((opt, index) => (
                <div key={ index } className='answer-box' onClick={() => handleOptionClick(index)}>
                    <h4>{ opt }</h4>
                </div>
            ))}
            {!(currentChoice === null) && (
                <h3>Current choice: {currentChoice}</h3>
            )}
            <div className="button-container">
                <button className='back-button' onClick={() => handleButtons('back')}><h4>Back</h4></button>
                {num === maxNum && (
                    <button className='submit-button' onClick={() => handleButtons('submit')}><h4>Submit</h4></button>
                )}
            </div>
        </div>
    );
}


export default QuizQuestions;

