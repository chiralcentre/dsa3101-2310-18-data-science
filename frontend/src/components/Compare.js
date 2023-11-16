import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";
import CompareResults from "./CompareResults"


const Compare = () => {
    const [uni1, setUni1] = useState("NUS")
    const [uni2, setUni2] = useState("NUS")
    const [courseList1, setCourseList1] = useState(["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics"])
    const [courseList2, setCourseList2] = useState(["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics"])
    const [course1, setCourse1] = useState("Data Science and Analytics")
    const [course2, setCourse2] = useState("Data Science and Analytics")
    const [display, setDisplay] = useState(false)
    const history = useHistory()

    const handleClick = () => {
        setDisplay(true)
        // history.push(`/compare?uni1=${uni1}major1=${course1}&uni2=${uni2}&major2=${course2}`)
    }

    const handleChange = (e, dropdown) => {
        if (dropdown === 1) {
            setUni1(e)
            setDisplay(false)
            if (uni1 === "NUS") {
                setCourseList1(["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics"])
                setCourse1("Data Science and Analytics")
            } if (uni1 === "NTU") {
                setCourseList1(["Data Science and Artificial Intelligence", "Economics and Data Science"])
                setCourse1("Data Science and Artificial Intelligence")
            } if (uni1 === "SMU") {
                setCourseList1(["Quantitative Finance", "Data Science and Analytics", "Information Systems(Business Analytics)"])
                setCourse1("Quantitative Finance")
            }
        } else if (dropdown === 2) {
            setUni2(e)
            setDisplay(false)
            if (uni2 === "NUS") {
                setCourseList2(["Data Science and Analytics", "Business Analytics", "Quantitative Finance", "Statistics", "Data Science and Economics"])
                setCourse2("Data Science and Analytics")
            } if (uni2 === "NTU") {
                setCourseList2(["Data Science and Artificial Intelligence", "Economics and Data Science"])
                setCourse2("Data Science and Artificial Intelligence")
            } if (uni2 === "SMU") {
                setCourseList2(["Quantitative Finance", "Data Science and Analytics", "Information Systems (Business Analytics)"])
                setCourse2("Quantitative Finance")
            }
        }
    }


    useEffect(() => {
        handleChange(uni1, 1)
    }, [uni1])

    useEffect(() => {
        handleChange(uni2, 2)
    }, [uni2])

    return (
        <div className="compare">
            <div className="container-heading">
                <h1 className="heading-title secondary">Compare Data Science Courses</h1>
                <p className="heading-subtitle-secondary">No more hassle in comparing data science courses from multiple resources. Try our comparison feature to discern the differences between two data science courses seamlessly.</p>
                <div className="circle-blue left smaller"></div>
                <div className="circle-purple left smaller"></div>
                <div className="circle-blue right smaller"></div>
                <div className="circle-purple right smaller"></div>
            </div>

            <div className="container-body margin-bottom">
                <div className="compare-dropdown">
                    <div className="dropdown">
                        <form>
                            <label>University</label>
                            <select value={uni1} onChange={(e) => { setUni1(e.target.value) }}>
                                <option value="NUS">NUS</option>
                                <option value="NTU">NTU</option>
                                <option value="SMU">SMU</option>
                            </select>

                            <label>Course</label>
                            <select value={course1} onChange={(e) => { setCourse1(e.target.value); setDisplay(false); }}>
                                {courseList1.map((course) => (<option value={course}>{course}</option>))}
                            </select>
                        </form>
                    </div>

                    <div className="dropdown">
                        <form>
                            <label>University</label>
                            <select value={uni2} onChange={(e) => { setUni2(e.target.value) }}>
                                <option value="NUS">NUS</option>
                                <option value="NTU">NTU</option>
                                <option value="SMU">SMU</option>
                            </select>

                            <label>Course</label>
                            <select value={course2} onChange={(e) => { setCourse2(e.target.value); setDisplay(false); }}>
                                {courseList2.map((course) => (<option value={course}>{course}</option>))}
                            </select>
                        </form>
                    </div>
                </div>

                <div className="button-container">
                    <button id='compare-button' className="btn btn--outline" onClick={() => handleClick()}>Compare</button>
                </div>


                {display && <CompareResults uni1={uni1} uni2={uni2} course1={course1} course2={course2} />}

            </div>
        </div>

    );
}

export default Compare;