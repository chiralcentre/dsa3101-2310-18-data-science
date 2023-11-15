import { Link } from 'react-router-dom';
import 'chart.js/auto';
import { Radar } from 'react-chartjs-2';
import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";


const Overview = () => {
    const [jobType, setJobType] = useState("Data Analyst");
    const [radarData, setRadarData] = useState(null);
    const history = useHistory();
    const [finalRadar, setFinalRadar] = useState(null);

    const jobColors = {
        "Data Analyst": { backgroundColor: 'rgba(35, 55, 126, 0.3)', borderColor: 'rgba(35, 55, 126, 0.8)' },
        "Data Scientist": { backgroundColor: 'rgba(126, 35, 35, 0.3)', borderColor: 'rgba(126, 35, 35, 0.8)' },
        "Quantitative Researcher": { backgroundColor: 'rgba(63, 191, 127, 0.3)', borderColor: 'rgba(63, 191, 127, 0.8)' },
        "Quantitative Analyst": { backgroundColor: 'rgba(242, 201, 76, 0.3)', borderColor: 'rgba(242, 201, 76, 0.8)' },
        "Business Analyst": { backgroundColor: 'rgba(79, 129, 189, 0.3)', borderColor: 'rgba(79, 129, 189, 0.8)' },
    };

    useEffect(() => {
        fetchJobDistribution();
    }, [jobType]);

    const fetchJobDistribution = async () => {
        try {
            const response = await fetch(`http://localhost:5000/job-distribution?job=${encodeURIComponent(jobType)}`);
            const data = await response.json();
            setRadarData(data);

        } catch (error) {
            console.error('Error fetching job distribution data:', error);
        }
    };

    useEffect(() => {
        if (radarData) {
            const numericValues = radarData.match(/[-+]?[0-9]*\.?[0-9]+/g);
            const keys = radarData.match(/"([^"]+)":/g);
            const numbersList = numericValues.map(Number);
            const cleanedKeys = keys.map((key) => key.replace(/["":]/g, ''));
    
            const radar = {
                labels: cleanedKeys.slice(1) || [], 
                datasets: [
                    {
                        label: jobType,
                        backgroundColor: jobColors[jobType].backgroundColor,
                        borderColor: jobColors[jobType].borderColor,
                        data: numbersList || [],
                    },
                ],
            };
            setFinalRadar(radar);
        }
    }, [radarData]);

    const option = {};
    
    return (
        <section className="section-overview">
            {/* <div className="overview"> */}
            <div className="container-heading">
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
                    <select value={jobType} onChange={(e) => { setJobType(e.target.value) }}>
                        <option value="Data Analyst">Data Analyst</option>
                        <option value="Data Scientist">Data Scientist</option>
                        <option value="Quantitative Researcher">Quantitative Researcher</option>
                        <option value="Quantitative Analyst">Quantitative Analyst</option>
                        <option value="Business Analyst">Business Analyst</option>
                    </select>
                </form>
            </div>

            <div className="result">
                {radarData ? (
                    <div className="chart">
                        {finalRadar && <Radar data={finalRadar} options={option} />}
                    </div>
                ) : (
                    <p>Loading...</p>
                )}
            </div>

        </section>
    );
}

export default Overview;