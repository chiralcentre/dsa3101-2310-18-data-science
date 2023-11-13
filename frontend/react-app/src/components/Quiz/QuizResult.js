import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const QuizResult = ({ choices }) => {
  const newList = Object.values(choices);
  const postFormat = { 0: 0, 1: 0, 2: 0, 3: 0 };
  const [result, setResult] = useState([]);

  newList.forEach((value) => {
    const stringValue = String(value);
    postFormat[stringValue] += 1;
  });

  async function getResult() {
    const res = await fetch("http://localhost:5000/quiz-results", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(postFormat),
    });
    const analysis = await res.json();
    setResult(analysis);
  }

  useEffect(() => {
    getResult();
  }, []);

  return (
    <div className="result-page">
      <div className="result-headline">
        <p>Your Quiz Result !</p>
      </div>
      <img src="/img/Result.png" alt="" className="result-page-img" />
      <div className="result-content">
        <div className="result-title">
          {" "}
          Based on your responses, here is our top recommendation for you :{" "}
        </div>
        <div className="result-desc">
          {result.reverse().map((ranking, index) => (
            <p key={index}>{`${index + 1}. ${ranking[1]} at ${
              ranking[0]
            } - Score: ${ranking[2].toFixed(2)}`}</p>
          ))}
        </div>
      </div>
      <Link to="/quiz">
        <button className="restart-quiz-button">Restart Quiz</button>
      </Link>
    </div>
  );
};

export default QuizResult;
