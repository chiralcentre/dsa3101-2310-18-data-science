import { Link } from "react-router-dom";
import Feedback from "./Feedback";

const Home = () => {
    return (
        <section className="section-home">
            <div className="container">
                <div className="home-title">
                    <h1 className="heading-primary"> Data Guru </h1>
                    <p className="heading-subtitle"> Your Guide to Data Science Education </p>
                    <a href="#section1" className="btn btn--outline bounce"> Get Started &darr;</a>
                </div>

                <div className="inline-block" id="section1">
                    <div className="inline-item-1">
                        <h2 className="heading-left">What is Data Science?</h2>
                        <p className="subtitle"> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>

                        <Link to="/overview">
                            <button className="btn btn--outline"> Learn More </button>
                        </Link>
                    </div>

                    <div className="inline-item-2">
                        <img src="img/home-1.png" className="home-illustration" />
                    </div>

                </div>

                <div className="home-features">
                    <h2 style={{padding: 0}}> What can we do for you? </h2>

                    <div className="inline-block">

                    <div className="inline-item-2"> 
                    <img src="img/home-2.png" className="home-illustration" />
                    <h2> Course Comparison </h2>
                    <p className="subtitle-center"> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    <Link to="/compare">
                        <button className="btn btn--outline"> Compare Now </button>
                    </Link>
                    </div>

                    <div className="inline-item-2"> 
                    <img src="img/home-3.png" className="home-illustration" />
                    <h2> Course Finder</h2>
                    <p className="subtitle-center"> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                    <Link to="/quiz">
                        <button className="btn btn--outline"> Take Quiz </button>
                    </Link>

                    </div>
                    </div>
                    
                </div>
            </div>
            <Feedback />
        </section>
    );
}

export default Home;