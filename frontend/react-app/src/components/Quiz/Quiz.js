import { useHistory } from 'react-router-dom';

const Quiz = () => {
    const history = useHistory();

    const handleClick = () => {
        history.push('/quiz/questions')
    }

    return (  
        <div className="quiz-start">
            <div>Find out your best course!</div>
            <img src="img/DataScientist.png" alt="" className="quiz-front" />
            <button onClick={handleClick} className="button-start">Start Quiz</button>
        </div>
    );
}
 
export default Quiz;