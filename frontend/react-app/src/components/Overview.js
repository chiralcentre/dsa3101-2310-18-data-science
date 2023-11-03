import {Link} from 'react-router-dom';

const Overview = () => {
    return (
        <section className="section-overview">
            <div className="overview">
                <div className="overview-header-container">
                    <h2 className="overview-header">What is Data Science?</h2>
                    <p className="overview-header-text">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                    </p>
                </div>

                <div className="column-container">
                    <div className="column">Graph 1</div>
                    <div className="column">Text 1</div>
                </div>

                <div className="column-container">
                    <div className="column">Text 2</div>
                    <div className="column">Graph 2</div>
                </div>

                <h4 className='button-text'>Explore the universities!</h4>

                <div className="buttonContainer">
                    <Link to="/NUS"><button className='button'> NUS </button></Link>
                    <Link to="/NTU"><button className='button'> NTU </button></Link>
                    <Link to="/SMU"><button className='button'> SMU </button></Link>
                </div>
            </div>
        </section>  
    );
}
 
export default Overview;