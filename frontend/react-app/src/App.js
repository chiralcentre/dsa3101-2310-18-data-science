import Navbar from "./components/Navbar";
import Home from "./components/Home";
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Overview from "./components/Overview";
import Compare from "./components/Compare";
import Quiz from "./components/Quiz";
import About from "./components/About";
import Footer from "./components/Footer";


function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route exact path="/">
          <Home />
        </Route>
        <Route path="/overview">
          <Overview />
        </Route>
        <Route path="/compare">
          <Compare />
        </Route>
        <Route path="/quiz">
          <Quiz />
        </Route>
        <Route path="/about">
          <About />
        </Route>
      </Switch>
      <Footer />
    </Router>
  );
}

export default App;
