import React, { useState, useEffect } from 'react';
import LoadingAnimation from './LoadingAnimation';
import { Link } from "react-router-dom";

const QuizResult = () => {
//   const [isLoadingComplete, setIsLoadingComplete] = useState(false);

//   const handleLoadingComplete = () => {
//     setIsLoadingComplete(true);
//   };

  useEffect(() => {
    // Scroll to the top of the page when the component mounts
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="quiz-result">
        <div className="result-page">
            <div className="result-title">Quiz Result</div>
            <img src="/img/Result.png" alt="" className='result-page-img'/>
            <div className="result-content">
                <div className="quiz-main">Based on your responses, we recommend you to take :</div>
                <div className="quiz-desc"><b>Data Science</b> at the <b>National University of Singapore!</b></div> 
            </div>        
            <Link to="/quiz"> 
                <button className="restart-quiz-button">Restart Quiz</button>
            </Link>
        </div>
      {/* {isLoadingComplete ? (
        <div className="result-page">
            Hello
        </div>
      ) : (
        <LoadingAnimation onLoadingComplete={handleLoadingComplete} />
      )} */}
    </div>
  );
}

export default QuizResult;
