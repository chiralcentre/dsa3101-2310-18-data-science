import { useHistory } from 'react-router-dom';

const Quiz = () => {
    const history = useHistory();

    const handleClick = () => {
        history.push('/quiz/questions')
    }

    return (  
        <div className="quiz">
            <h2>Find out your best course!</h2>
            <img src="img/DataScientist.png" alt="" className="quiz-front" />
            <button onClick={handleClick}>Start Now!</button>
        </div>
    );
}
 
export default Quiz;