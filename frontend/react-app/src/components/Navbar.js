// import {Link, NavLink} from "react-router-dom";

const Navbar = () => {
    return (
            <header className="header">
                <a href="#">
                    <img className="logo" alt="logo" src="img/logo.png" />
                </a>

                <nav>
                    <ul className="main-nav-list">
                        <li><a className="main-nav-link" href="#">Home</a></li>
                        <li><a className="main-nav-link" href="#overview">Overview</a></li>
                        <li><a className="main-nav-link" href="#compare">Compare</a></li>
                        <li><a className="main-nav-link" href="#quiz">Quiz</a></li>
                        <li><a className="main-nav-link" href="#about">About</a></li>
                    </ul>
                </nav>
            </header>

    );
}

export default Navbar;