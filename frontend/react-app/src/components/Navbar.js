import { NavLink } from 'react-router-dom';

const Navbar = () => {
    return (
            <header className="header">
                {/* <Link to="/">
                    <img
                        className="navbar-logo"
                        alt="logo"
                        src="img/logo.png"
                    />
                </Link> */}
                {/* <img className="navbar-logo" alt="logo" src="img/logo2.png" /> */}
                <h1 className="navbar-logo">DATAGURU</h1>
                <ul className="nav__links">
                    <li><NavLink exact to="/" activeClassName="active">Home</NavLink></li>
                    <li><NavLink to="/overview" activeClassName="active">Data Science</NavLink></li>
                    <li><NavLink to="/compare" activeClassName="active">Compare</NavLink></li>
                    <li><NavLink to="/quiz" activeClassName="active">Quiz</NavLink></li>
                    <li><NavLink to="/about" activeClassName="active">About</NavLink></li>
                </ul>
                <a class="contact-button" href="a"><button>Contact Us</button></a>
            </header>
    );
}

export default Navbar;