import { NavLink } from 'react-router-dom';
import React, { useState } from "react";
// import { Link } from "react-router-dom";
import { navItems } from "./NavItems";
import Dropdown from "./Dropdown";

const Navbar = () => {
    const [dropdown, setDropdown] = useState(false);

    return (
        <header className="header">
            <h2 className="navbar-logo">DG.</h2>

            <nav>
                <ul className="nav-list">
                    {navItems.map((item) => {
                        if (item.title === "Overview") {
                            return (
                                <li
                                    key={item.id}
                                    onMouseEnter={() => setDropdown(true)}
                                    onMouseLeave={() => setDropdown(false)}
                                >
                                    <NavLink className="nav-link" to={item.path}>{item.title} &#x25BE; </NavLink>
                                    {dropdown && <Dropdown />}
                                </li>
                            );
                        }
                        else if (item.title === "Home") {
                            return (
                                <li key={item.id}>
                                <NavLink className="nav-link" exact to={item.path}>{item.title}</NavLink>
                            </li>
                            );
                        }
                        else {
                            return (
                                <li key={item.id}>
                                    <NavLink className="nav-link" to={item.path}>{item.title}</NavLink>
                                </li>
                            );
                        }
                    })}
                </ul>
            </nav>
        </header>
    );
}

export default Navbar;