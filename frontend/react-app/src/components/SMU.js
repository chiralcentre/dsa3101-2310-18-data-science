import { Link } from 'react-router-dom';

const SMU = () => {
    return (
        <section>
            <div className="container-heading">
                <h1 className="heading-title primary">SMU</h1>
                <h4 className="heading-subtitle">Singapore Management University</h4>
            </div>

            <div className="container-body">
                <div className="inline-block">

                    <div className="inline-item-1">
                        <h2 className="subheading-title left">General Information</h2>
                        <p className="subheading-subtitle-secondary">
                            The Singapore Management University (SMU) is a publicly-funded private university in Singapore. Founded in 2000, SMU is the third oldest autonomous university in the country, and models its education after the Wharton School. It is also the only university in Singapore with a city campus. The university was also awarded triple accreditation by AACSB, EQUIS and AMBA.
                        </p>
                    </div>

                    <div className="inline-item-2">
                        <img src="img/smu-pic.jpg" className='illustration' />
                    </div>
                </div>

                <h4 className="university-course-header">Available Data Related Courses</h4>

                <div className='button-course-container'>
                    <a href='https://economics.smu.edu.sg/bachelor-science-economics/curriculum/2nd-major-data-science-and-analytics' target="_blank"><button className='button-course'>
                        <p className='course-name'> Data Science and Analytics </p>
                        <p className='course-department'> School of Economics </p>
                        <p className='course-description'> Second major in Data Science and Analytics is offered in SMU as part of the Bachelor of Science in Economics program. It enables you to transform data into valuable insights, addressing the rising demand for data scientists and analysts. It equips you with essential data skills in programming languages like R, Python, and SQL, covering database querying, data pipeline development, and interactive visualizations using JavaScript libraries. DSA also delves into statistical learning, empowering you to build and test models for data description and prediction. You'll gain a competitive edge by mastering skills relevant to the future workforce, including big data technologies like MySQL, Hadoop, and Spark. Practical application is emphasized, with a focus on effectively communicating analysis results, using platforms like GitHub and GitHub Pages, and building a portfolio for internship and job interviews.  </p>
                    </button></a>

                    <a href='https://scis.smu.edu.sg/bsc-information-systems' target="_blank"><button className='button-course'>
                        <p className='course-name'> Information Systems (Business Analytics) </p>
                        <p className='course-department'> School of Computing and Information Systems </p>
                        <p className='course-description'> Technology advancement provides many exciting opportunities for companies to improve their business processes and society to improve the quality of life in this digital economy. Our Bsc (IS) Information Systems programme teaches students the business and technology skills to create value for businesses and society in their digital business transformation journey. Students learn to use data analytics to discover organisational issues and innovate digital business solutions to drive digital transformation.  </p>
                    </button></a>

                    <a href='https://business.smu.edu.sg/disciplines/quantitative-finance' target="_blank"><button className='button-course'>
                        <p className='course-name'> Quantitative Finance </p>
                        <p className='course-department'> Lee Kong Chian School of Business </p>
                        <p className='course-description'> With a QF major, you are in a good position to wow job interviewers and headhunters seeking to employ risk analysts, junior quant research strategists, and in time to come, specialist leaders. SMU's QF courses will let you see for yourselves how cool it can be that math can help an investment/trading firm in generating revenues while limiting its risk exposures. You will also learn to write computer codes to analyze data for risk management and for research in creating new quantitative trading strategies.</p>
                    </button></a>

                </div>

                <h2 className="subheading-title center"> Explore the universities and its majors below! </h2>

                <div className="container-button longer">
                    <Link to="/NUS" onClick={() => { window.scroll(0, 0); }}><button className='button-uni btn--outline'> NUS </button></Link>
                    <Link to="/NTU" onClick={() => { window.scroll(0, 0); }}><button className='button-uni btn--outline'> NTU </button></Link>
                    <Link to="/SMU" onClick={() => { window.scroll(0, 0); }}><button className='button-selected btn--outline'> SMU </button></Link>
                </div>

            </div>
        </section>
    );
}

export default SMU;