import { Link } from 'react-router-dom';

const NTU = () => {
    return (
        <section>
            <div className="container-heading">
                <h1 className="heading-title primary">NTU</h1>
                <h4 className="heading-subtitle">Nanyang Technological University</h4>
                <div className="circle-blue left smaller"></div>
                <div className="circle-purple left smaller"></div>
                <div className="circle-blue right smaller"></div>
                <div className="circle-purple right smaller"></div>
            </div>

            <div className="container-body">
                <div className="inline-block">

                    <div className="inline-item-1">
                        <h2 className="subheading-title left">General Information</h2>
                        <p className="subheading-subtitle-secondary">
                            Nanyang Technological University (NTU) is one of Singapore's two major national universities. Founded in 1981, it is also the second-oldest autonomous university in the country. NTU is frequently ranked within the world's top 30 universities according to most major international rankings, and is widely-considered to be one of the two most prestigious universities in Singapore, after the National University of Singapore.
                        </p>
                    </div>

                    <div className="inline-item-2">
                        <img src="img/ntu-ranking.jpg" className='illustration' />
                    </div>

                </div>

                <h4 className="university-course-header">Available Data Related Courses</h4>

                <div className='button-course-container'>
                    <a href='https://www.ntu.edu.sg/education/undergraduate-programme/bachelor-of-science-in-data-science-artificial-intelligence' target="_blank"><button className='button-course'>
                        <p className='course-name'> Data Science and Artificial Intelligence </p>
                        <p className='course-department'> School of Computer Science and Engineering (SCSE)  </p>
                        <p className='course-description'> An undergraduate degree programme in Data Science and Artificial Intelligence, based on rigorous training in the synergistic fields of statistics and computer science. The programme, which is run jointly by the School of Computer Science and Engineering and the School of Physical and Mathematical Sciences, targets students who have the vision of using data science and artificial intelligence (AI) to find innovative solutions to society’s pressing challenges. The curriculum provides students with opportunities to solve real-life problems in different applications domains ranging from science and technology, healthcare, business and finance, environmental sustainability, and more. </p>
                    </button></a>

                    <a href='https://www.ntu.edu.sg/education/undergraduate-programme/bachelor-of-science-in-economics-and-data-science' target="_blank"><button className='button-course'>
                        <p className='course-name'>  Economics and Data Sciences </p>
                        <p className='course-department'> School of Computer Science and Engineering (SCSE) </p>
                        <p className='course-description'> This is a four-year degree programme in which undergraduate students will read 3 subject areas in Economics, Mathematics and Data Science. The programme provides its students with a strong foundation in Economics and subsequently prepares them not only to handle and deal with big data through Data Science but also develops their ability to make economic sense from their applications in modern large-scale data analysis.  Upon graduation, students are expecting to work as data analysts, data scientists, economists and industry analysts who are skillful in analyzing big data.​ </p>
                    </button></a>

                </div>


                <h2 className="subheading-title center"> Explore the universities and its majors below! </h2>

                <div className="container-button longer">
                    <Link to="/NUS" onClick={() => { window.scroll(0, 0); }}><button className='button-uni btn--outline'> NUS </button></Link>
                    <Link to="/NTU" onClick={() => { window.scroll(0, 0); }}><button className='button-selected btn--outline'> NTU </button></Link>
                    <Link to="/SMU" onClick={() => { window.scroll(0, 0); }}><button className='button-uni btn--outline'> SMU </button></Link>
                </div>
            </div>
        </section>
    );
}

export default NTU;