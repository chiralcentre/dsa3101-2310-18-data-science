import React, { useEffect } from 'react';

const LoadingAnimation = ({ onLoadingComplete }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onLoadingComplete(); 
    }, 3000); 
    return () => clearTimeout(timer);
  }, [onLoadingComplete]);

  return (
    <div className="loading-container">
        <span className="loading-span loading-one"></span>
        <span className="loading-span loading-two"></span>
        <span className="loading-span loading-three"></span>
        <span className="loading-span loading-four"></span>
    </div>
  );
}

export default LoadingAnimation;
