import Navbar from "./components/Navbar";
import Home from "./components/Home";
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Overview from "./components/Overview";
import Compare from "./components/Compare";

import NUS from "./components/NUS";
import NTU from "./components/NTU";
import SMU from "./components/SMU";

import Quiz from "./components/Quiz/Quiz";
import QuizQuestions from "./components/Quiz/QuizQuestions";
import QuizResult from "./components/Quiz/QuizResult";

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
        <Route exact path="/quiz">
          <Quiz />
        </Route>
        <Route path="/quiz/questions">
          <QuizQuestions />
        </Route>
        <Route path="/about">
          <About />
        </Route>
        <Route path="/NUS" component={NUS} />
        <Route path="/NTU" component={NTU} />
        <Route path="/SMU" component={SMU} />
      </Switch>
      <Footer />
    </Router>
  );
}

export default App;
