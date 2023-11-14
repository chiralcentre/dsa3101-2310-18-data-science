import { Link } from "react-router-dom";
import Feedback from "./Feedback";

const Home = () => {
    return (
        <section>
            <div className="container-heading wide-padding">
                <h1 className="heading-title primary"> Data Guru </h1>
                <p className="heading-subtitle"> Your Guide to Data Science Education </p>
                <div className="circle-blue left"></div>
                <div className="circle-purple left"></div>
                <div className="circle-blue right"></div>
                <div className="circle-purple right"></div>
                <a href="#overview" className="btn btn--outline bounce"> Get Started &darr; </a>
                
            </div>

            <div className="container-body">
                <div className="funfact">
                    <h3> DO YOU KNOW? </h3>
                    <p className="italic"> “Data science was identified as the skill with the largest skill gap, according to a 2021 report by the <a href="https://www3.weforum.org/docs/WEF_Future_of_Jobs_2020.pdf" target="_blank">World Economic Forum</a>.”
                    </p>
                </div>

                <div className="inline-block" id="overview">
                    <div className="inline-item-1">
                        <span className="subheading"> Overview </span>
                        <h2 className="subheading-title left"> What is Data Science? </h2>
                        <p className="subheading-subtitle-secondary"> Understand what data science comprises by knowing the skills learned in data science courses and the job prospects in the data industry. </p>

                        <Link to="/overview" onClick={() => { window.scroll(0, 0); }}>
                            <button className="btn btn--outline"> Learn More </button>
                        </Link>
                    </div>

                    <div className="inline-item-2">
                        <img src="img/home-1.png" className="illustration" />
                    </div>

                </div>

                <span className="subheading center"> Features </span>
                <h2 className="subheading-title center"> What can we do for you? </h2>

                <div className="inline-block">
                    <div className="inline-item-2">
                        <div className="card">
                            <img src="img/home-2.png" className="illustration" />
                            <h2 className="subheading-title center"> Course Comparison </h2>
                            <p className="subheading-subtitle-card"> No more hassle in comparing data science courses from multiple resources. Try our comparison feature to discern the differences between two data science courses seamlessly. </p>
                            <Link to="/compare" onClick={() => { window.scroll(0, 0); }}>
                                <button className="btn btn--outline"> Compare Now </button>
                            </Link>
                        </div>
                    </div>

                    <div className="inline-item-2">
                        <div className="card">
                            <img src="img/home-3.png" className="illustration" />
                            <h2 className="subheading-title center"> Course Finder </h2>
                            <p className="subheading-subtitle-card"> Get personalized recommendation for the best data science courses that align with your skills and preferences by taking our quiz, specially tailored for you. </p>
                            <Link to="/quiz" onClick={() => { window.scroll(0, 0); }}>
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