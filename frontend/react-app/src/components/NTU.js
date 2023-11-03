import {Link} from 'react-router-dom';

const NTU = () => {
    return (  
        <div className="university">
            <h2 className="university-header">NTU</h2>
            <h4 className="university-subheader">Nanyang Technological University</h4>
            <div className="column-container">
                <div className="column">Graph 1</div>
                <div className="column">Text 1</div>
            </div>

            <div className="column-container">
                <div className="column">Text 2</div>
                <div className="column">Graph 2</div>
            </div>

            <h4 className="module-distribution">Module Distribution</h4>

            <div className="column-container">
                <div className="column">Piechart</div>
                <div className="column">
                    <h4>25% Finance</h4> <br></br>
                    <h4>25% Programming</h4> <br></br>
                    <h4>25% Data Analysis/Modelling</h4> <br></br>
                    <h4>25% Statistics</h4>
                </div>
            </div>

            <h4 className="modules">Modules</h4>

            <div className="module-list">
                <ol>
                    <li><a href="https://nusmods.com/courses/DSA1101/introduction-to-data-science">NTU MOD 1</a>: Introduction to Data Science</li>
                    <li><a href="https://nusmods.com/courses/DSA2101/essential-data-analytics-tools-data-visualisation">NTU MOD 2</a>: Essential Data Analytics Tools: Data Visualisation</li>
                    <li><a href="https://nusmods.com/courses/DSA2102/essential-data-analytics-tools-numerical-computation">NTU MOD 3</a>: Essential Data Analytics Tools: Numerical Computation</li>
                </ol>

            </div>
            

            <h4 className='button-text'>Explore the universities!</h4>

            <div className="buttonContainer">
                <Link to="/NUS"><button className='button'> NUS </button></Link>
                <Link to="/NTU"><button className='button-selected'> NTU </button></Link>
                <Link to="/SMU"><button className='button'> SMU </button></Link>
            </div>

        </div>

        
    );
}
 
export default NTU;