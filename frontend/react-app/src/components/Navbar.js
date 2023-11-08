import {NavLink} from "react-router-dom";

const Navbar = () => {
    return (
            <header className="header">
                {/* <a href="#">
                    <img className="logo" alt="logo" src="img/logo.png" />
                </a> */}
                <h2 className="logo">DG.</h2>

                <nav>
                    <ul className="main-nav-list">
                        <li><NavLink className="main-nav-link" exact to="/">Home</NavLink></li>
                        <li><NavLink className="main-nav-link" to="/overview">Overview</NavLink></li>
                        <li><NavLink className="main-nav-link" to="/compare">Compare</NavLink></li>
                        <li><NavLink className="main-nav-link" to="/quiz">Quiz</NavLink></li>
                        <li><NavLink className="main-nav-link" to="/about">About</NavLink></li>
                    </ul>
                </nav>
            </header>

    );
}

export default Navbar;