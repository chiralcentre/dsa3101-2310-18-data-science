import {Link} from 'react-router-dom';

const NTU = () => {
    return (  
        <div className="university">
            <h2 className="university-header">NTU</h2>
            <h4 className="university-subheader">Nanyang Technological University</h4>
            <p className="overview-header-text">
                Data science is a multidisciplinary field that involves the use of various techniques, algorithms, processes, and systems to extract knowledge and insights from structured and unstructured data. 
            </p>

            <div className="overview-inline-block">

                <div className="overview-inline-item-1">
                    <p className="overview-cluster-header-1">General Information</p>
                    <p className="overview-inline-text-1"> 
                    Nanyang Technological University (NTU) is one of Singapore's two major national universities. Founded in 1981, it is also the second-oldest autonomous university in the country. NTU is frequently ranked within the world's top 30 universities according to most major international rankings, and is widely-considered to be one of the two most prestigious universities in Singapore, after the National University of Singapore.
                    </p>
                </div>

                <div className="overview-inline-item-2">
                    <img src="img/ntu-ranking.jpg" className='ntu-img1'/>
                </div>

            </div>   

            <h4 className="university-course-header">Available Data Related Courses</h4>

            <div className='button-course-container'>
                <a href='https://www.ntu.edu.sg/education/undergraduate-programme/bachelor-of-science-in-data-science-artificial-intelligence'><button className='button-course'>
                    <p className='course-name'> Data Science and Artificial Intelligence </p>
                    <p className='course-department'> School of Computer Science and Engineering (SCSE)  </p>
                    <p className='course-description'> An undergraduate degree programme in Data Science and Artificial Intelligence, based on rigorous training in the synergistic fields of statistics and computer science. The programme, which is run jointly by the School of Computer Science and Engineering and the School of Physical and Mathematical Sciences, targets students who have the vision of using data science and artificial intelligence (AI) to find innovative solutions to society’s pressing challenges. The curriculum provides students with opportunities to solve real-life problems in different applications domains ranging from science and technology, healthcare, business and finance, environmental sustainability, and more. </p>
                </button></a>

                <a href='https://www.ntu.edu.sg/education/undergraduate-programme/bachelor-of-science-in-economics-and-data-science'><button className='button-course'>
                    <p className='course-name'>  Economics and Data Sciences </p>
                    <p className='course-department'> School of Computer Science and Engineering (SCSE) </p>
                    <p className='course-description'> This is a four-year degree programme in which undergraduate students will read 3 subject areas in Economics, Mathematics and Data Science. The programme provides its students with a strong foundation in Economics and subsequently prepares them not only to handle and deal with big data through Data Science but also develops their ability to make economic sense from their applications in modern large-scale data analysis.  Upon graduation, students are expecting to work as data analysts, data scientists, economists and industry analysts who are skillful in analyzing big data.​ </p>
                </button></a>

            </div>
            

            <h4 className='button-text'>Explore the universities and its majors below!</h4>

            <div className="buttonContainer">
                <Link to="/NUS"><button className='button-uni'> NUS </button></Link>
                <Link to="/NTU"><button className='button-selected'> NTU </button></Link>
                <Link to="/SMU"><button className='button-uni'> SMU </button></Link>
            </div>

        </div>

        
    );
}
 
export default NTU;