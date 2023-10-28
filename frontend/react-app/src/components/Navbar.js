import {Link} from "react-router-dom";

const Navbar = () => {
    return (
            <header className="header">
                <a href="#">
                    <img className="logo" alt="logo" src="img/logo.png" />
                </a>

                <nav>
                    <ul className="main-nav-list">
                        <li><Link className="main-nav-link" to="/">Home</Link></li>
                        <li><Link className="main-nav-link" to="/overview">Overview</Link></li>
                        <li><Link className="main-nav-link" to="/compare">Compare</Link></li>
                        <li><Link className="main-nav-link" to="/quiz">Quiz</Link></li>
                        <li><Link className="main-nav-link" to="/about">About</Link></li>
                    </ul>
                </nav>
            </header>

    );
}

export default Navbar;