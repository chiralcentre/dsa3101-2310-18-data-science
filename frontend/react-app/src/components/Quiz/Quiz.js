import { useHistory } from 'react-router-dom';

const Quiz = () => {
    const history = useHistory();

    const handleClick = () => {
        history.push('/quiz/questions')
    }

    return (  
        <div className="quiz-start">
            <div className='container-1'>
                <div class="box1">
                    <div className="quiz-title">Discover Your Data Potential !<br /></div>
                    <div className='quiz-desc'>Take our quiz to find out now!</div>
                </div>
                <div class="box2"><button onClick={handleClick} className="button-start">Start Quiz</button></div>
            </div>
            <div className='container-2'>
                <img src="img/DataScientist.png" alt="" className="quiz-img" />
            </div>
        </div>
    );
}
 
export default Quiz;