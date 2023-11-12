import { Link } from 'react-router-dom';
import 'chart.js/auto';
import { Radar } from 'react-chartjs-2';
import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

const Overview = () => {
    const [uni2, setUni2] = useState("Data Analyst")
    const [courseList2, setCourseList2] = useState(["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics"])
    const [course2, setCourse2] = useState("")
    const [display, setDisplay] = useState(false)
    const history = useHistory()


    const radar = {
        labels: ['Finance/Economics', 'Programming/Algorithm', 'Data Analysis/Modelling', 'Statistics'],
        datasets: [
            {
                label: `${uni2} ${course2}`,
                backgroundColor: '#23377E',
                borderColor: 'black',
                data: [0.2, 0.3, 0.1, 0.4]
            },
        ],
    };

    const option = {

    };


    return (
        <section className="section-overview">
            {/* <div className="overview"> */}
            <div className="overview-header-container">
                <h1 className="heading-secondary">What is Data Science?</h1>
                <p className="subtitle-secondary">
                    Data science is a multidisciplinary field that involves the use of various techniques, algorithms, processes, and systems to extract knowledge and insights from structured and unstructured data.
                </p>
            </div>

            <div className="overview-subheader-container">
                <h2 className="overview-subheader">Skills Learned in Data Science Course</h2>
                <p className="overview-subheader-text"> Based on our analysis of data science related courses in Top 3 Universities in Singapore, we managed to get distribution of topics that are commonly learned in data science courses.
                </p>
            </div>

            <div className="overview-inline-block">

                <div className="overview-inline-item-1">
                    <p className="overview-number-1">01</p>
                    <p className="overview-cluster-header-1">Algorithms and Numerical Methods</p>
                    <p className="overview-inline-text-1">
                        Algorithms are the backbone of data science, enabling efficient data processing, analysis, and pattern recognition. Data scientists must have a strong foundation in various algorithms to manipulate and extract insights from datasets. Numerical methods play a vital role in solving mathematical problems in data science, especially when analytical solutions are not readily available, making them essential for tasks like optimization, simulation, and solving complex equations.
                    </p>
                </div>

                <div className="overview-inline-item-2">
                    <img src="img/overview-1.png" className='overview-img1' />
                </div>

            </div>

            <div className="overview-inline-block">

                <div className="overview-inline-item-3">
                    <img src="img/overview-2.png" className='overview-img2' />
                </div>

                <div className="overview-inline-item-4">
                    <p className="overview-number-2">02</p>
                    <p className="overview-cluster-header-2">Math and Statistics</p>
                    <p className="overview-inline-text-2">
                        Mathematics provides the fundamental tools for data science, including concepts like linear algebra, calculus, and discrete mathematics, which are crucial for building and understanding data science algorithms and models. Statistics is equally vital, empowering data scientists to draw meaningful conclusions from data through descriptive and inferential statistical techniques, hypothesis testing, and probability theory.
                    </p>
                </div>

            </div>

            <div className="overview-inline-block">

                <div className="overview-inline-item-1">
                    <p className="overview-number-1">03</p>
                    <p className="overview-cluster-header-1">Machine Learning</p>
                    <p className="overview-inline-text-1">
                        Machine learning is the heart of data science, encompassing techniques that enable algorithms and models to learn patterns from data and make predictions. Data science courses cover a wide array of machine learning methods, including supervised learning for prediction, unsupervised learning for clustering, and reinforcement learning for decision-making. Students also delve into algorithms like decision trees, neural networks, and support vector machines, along with model evaluation techniques to assess the performance of predictive models.
                    </p>
                </div>

                <div className="overview-inline-item-2">
                    <img src="img/overview-3.png" className='overview-img3' />
                </div>

            </div>


            <div className="overview-inline-block">

                <div className="overview-inline-item-3">
                    <img src="img/overview-4.png" className='overview-img4' />
                </div>

                <div className="overview-inline-item-4">
                    <p className="overview-number-2">04</p>
                    <p className="overview-cluster-header-2">Project Management</p>
                    <p className="overview-inline-text-2">
                        Project management skills are essential for ensuring that data science projects are successfully executed. This includes effective project planning, scoping, resource allocation, and timely completion of objectives. Communication and collaboration are equally critical, as data scientists often work in interdisciplinary teams, necessitating the ability to convey complex technical concepts to non-technical stakeholders and ensuring that data insights are effectively communicated and applied for informed decision-making.
                    </p>
                </div>

            </div>



            <h4 className='button-text'>Explore the universities and its majors below!</h4>

            <div className="buttonContainer">
                <Link to="/NUS" onClick={() => {window.scroll(0, 0);}}> <button className='button-uni btn--outline'> NUS </button></Link>
                <Link to="/NTU" onClick={() => {window.scroll(0, 0);}}> <button className='button-uni btn--outline'> NTU </button></Link>
                <Link to="/SMU" onClick={() => {window.scroll(0, 0);}}> <button className='button-uni btn--outline'> SMU </button></Link>
            </div>

            <div className="overview-job-container">
                <h2 className="overview-job-header">Job Prospects in Data Industry</h2>
                <p className="overview-job-text"> Based on the collected data from job postings in the data industry, the graph below illustrates the distribution of skills required for various roles.
                </p>
            </div>

            <div className="overview-dropdown">
                <form>
                    <select value={uni2} onChange={(e) => { setUni2(e.target.value) }}>
                        <option value="Data Analyst">Data Analyst</option>
                        <option value="Data Scientist">Data Scientist</option>
                        <option value="Quantitative Researcher">Quantitative Researcher</option>
                        <option value="Quantitative Analyst">Quantitative Analyst</option>
                        <option value="Business Analyst">Business Analyst</option>
                    </select>
                </form>
            </div>

            <div className="result">
                <div className="chart">
                    <Radar data={radar} options={option} />
                </div>
            </div>

            {/* </div> */}
        </section>
    );
}

export default Overview;