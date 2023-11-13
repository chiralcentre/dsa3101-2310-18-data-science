import { Link } from 'react-router-dom';

const NUS = () => {
    return (
        <section>
            <div className="container-heading">
                <h1 className="heading-title primary">NUS</h1>
                <h4 className="heading-subtitle">National University of Singapore</h4>
            </div>

            <div className="container-body">
                <div className="inline-block">

                    <div className="inline-item-1">
                        <h2 className="subheading-title left">General Information</h2>
                        <p className="subheading-subtitle-secondary">
                            The National University of Singapore (NUS) is a national public collegiate and research university in Singapore. Founded in 1905 as the Straits Settlements and Federated Malay States Government Medical School, NUS is the oldest autonomous university in Singapore. In a historic first for the University, NUS has broken into the worldwide top 10, according to results from the latest Quacquarelli Symonds (QS) World University Rankings (WUR) released on 28 June 2023. Now ranking 8th in the world, NUS is also the top university in Asia.
                        </p>
                    </div>

                    <div className="inline-item-2">
                        <img src="img/nus-ranking.jpg" className='illustration bigger' />
                    </div>
                </div>

                <h4 className="university-course-header">Available Data Related Courses</h4>

                <div className='button-course-container'>
                    <a href='https://www.stat.nus.edu.sg/prospective-students/undergraduate-programme/data-science-and-analytics/' target="_blank"><button className='button-course'>
                        <p className='course-name'> Data Science and Analytics </p>
                        <p className='course-department'> College of Humanities and Sciences (CHS) </p>
                        <p className='course-description'> Bachelor of Science (Honours) with Major in Data Science and Analytics. The four-year direct Honours programme is designed to prepare graduates who are ready to acquire, manage and explore data that will inspire change around the world. Students will read courses in Mathematics, Statistics and Computer Science, and be exposed to the interplay between these three key areas in the practice of data science. </p>
                    </button></a>

                    <a href='https://www.stat.nus.edu.sg/prospective-students/undergraduate-programme/data-science-and-analytics/' target="_blank"><button className='button-course'>
                        <p className='course-name'> Data Science and Economics </p>
                        <p className='course-department'> College of Humanities and Sciences (CHS) </p>
                        <p className='course-description'> Bachelor of Science (Honours) with Major in Data Science and Economics. The Data Science and Economics (DSE) cross-disciplinary programme (XDP) aims to produce students who have strong foundation knowledge in data science and economics as well as hands-on experience with empirical analysis of economic data, to analyse and interpret the local and global impact of data on individuals, organisation, society and the global economic ecosystem. </p>
                    </button></a>

                    <a href='https://www.math.nus.edu.sg/ug/majmin/primajors/qf/' target="_blank"><button className='button-course'>
                        <p className='course-name'> Quantitative Finance </p>
                        <p className='course-department'> College of Humanities and Sciences (CHS) </p>
                        <p className='course-description'> Bachelor of Science (Honours) with Major in Quantitative Finance. The NUS Quantitative Finance curriculum gives you an integrated overview of how mathematical methods and computing techniques are applied to finance, including mathematical theory, statistical tools, computing theory, financial principles and core financial product knowledge.</p>
                    </button></a>

                    <a href='https://www.stat.nus.edu.sg/' target="_blank"><button className='button-course'>
                        <p className='course-name'> Statistics </p>
                        <p className='course-department'> College of Humanities and Sciences (CHS) </p>
                        <p className='course-description'> Bachelor of Science (Honours) with Major in Statistics. Professors in the department prepare students in this four-year direct Honours programme for the workplace by teaching them how to collect, analyse and present data. Students learn how to extract information from surveys, databases and carefully designed experiments, in order to obtain understanding of the underlying phenomenon, or to decide on a suitable course of action. They learn programming, problem solving and data visualization skills, and they become sensitive to the applications at hand. </p>
                    </button></a>

                    <a href='https://www.comp.nus.edu.sg/programmes/ug/ba/curr/' target="_blank"><button className='button-course'>
                        <p className='course-name'> Business Analytics </p>
                        <p className='course-department'> School of Computing </p>
                        <p className='course-description'> The Bachelor of Science (Business Analytics) degree programme is an inter-disciplinary undergraduate degree programme offered by the School of Computing with participation from the Business School, Faculty of Engineering, Faculty of Science, and Faculty of Arts and Social Sciences. This is a four-year direct honours programme which offers a common two-year broad-based inter-disciplinary curriculum where all students will read courses in Mathematics, Statistics, Economics, Accounting, Marketing, Decision Science, Industrial and Systems Engineering, Computer Science and Information Systems. </p>
                    </button></a>
                </div>

                <h2 className="subheading-title center"> Explore the universities and its majors below! </h2>

                <div className="container-button longer">
                    <Link to="/NUS" onClick={() => { window.scroll(0, 0); }}><button className='button-selected btn--outline'> NUS </button></Link>
                    <Link to="/NTU" onClick={() => { window.scroll(0, 0); }}><button className='button-uni btn--outline'> NTU </button></Link>
                    <Link to="/SMU" onClick={() => { window.scroll(0, 0); }}><button className='button-uni btn--outline'> SMU </button></Link>
                </div>
            </div>
        </section>
    );
}

export default NUS;