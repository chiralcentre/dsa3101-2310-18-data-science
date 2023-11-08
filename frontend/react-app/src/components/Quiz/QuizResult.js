import React, { useState, useEffect } from 'react';
import LoadingAnimation from './LoadingAnimation';

const QuizResult = () => {
  const [isLoadingComplete, setIsLoadingComplete] = useState(false);

  const handleLoadingComplete = () => {
    setIsLoadingComplete(true);
  };

  useEffect(() => {
    // Scroll to the top of the page when the component mounts
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="quiz-result">
      {isLoadingComplete ? (
        <div className="result-page">

        </div>
      ) : (
        <LoadingAnimation onLoadingComplete={handleLoadingComplete} />
      )}
    </div>
  );
}

export default QuizResult;
