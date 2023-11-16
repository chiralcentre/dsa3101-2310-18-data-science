import 'chart.js/auto';
import { useEffect, useState } from 'react';
import { Radar } from 'react-chartjs-2';

const CompareResults = ({uni1, uni2, course1, course2}) => {
    const [distribution1, setDistribution1] = useState(null)
    const [distribution2, setDistribution2] = useState(null)
    const [data1, setData1] = useState(null)

    useEffect(() => {
        fetch(`http://localhost:5000/course-distribution?university=${uni1}&major=${course1}`)
        .then(res => {
            return res.json()
        })
        .then(data => {
            setDistribution1(JSON.parse(data))
        });
    }, []);

    useEffect(() => {
        fetch(`http://localhost:5000/course-distribution?university=${uni2}&major=${course2}`)
        .then(res => {
            return res.json()
        })
        .then(data => {
            setDistribution2(JSON.parse(data))
        });
    }, []);

    // const [dist1, setDist1] = useState([])
    // const [dist2, setDist2] = useState([])

    // useEffect(() => {
    //     if (uni1 === 'NUS') {
    //         if (course1 === 'Data Science and Analytics') {
    //             setDist1([55.4, 4.3, 3.5, 36.8])
    //         } else if (course1 === 'Business Analytics') {
    //             setDist1([34, 20.8, 32.6, 12.6])
    //         } else if (course1 === 'Quantitative Finance') {
    //             setDist1([28.6, 4.9, 18, 48.5])
    //         } else if (course1 === 'Statistics') {
    //             setDist1([34, 6.4, 7.5, 52.1])
    //         } else if (course1 === 'Data Science and Economics') {
    //             setDist1([50, 24.6, 3.3, 22.1])
    //         }
    //     } else if (uni1 === 'NTU') {
    //         if (course1 === 'Data Science and Artificial Intelligence') {
    //             setDist1([46.8, 14.2, 21.8, 17.2])
    //         } else if (course1 === 'Economics and Data Science') {
    //             setDist1([27.8, 34.3, 24, 13.9])
    //         }
    //     } else if (uni1 === 'SMU') {
    //         if (course1 === 'Quantitative Finance') {
    //             setDist1([19.2, 2.6, 60.9, 17.3])
    //         } else if (course1 === 'Data Science and Analytics') {
    //             setDist1([48.4, 14.8, 22.2, 14.5])
    //         } else if (course1 === 'Information Systems (Business Analytics)') {
    //             setDist1([26.7, 32.9, 39.9, 0.5])
    //         }
    //     }

    //     if (uni2 === 'NUS') {
    //         if (course2 === 'Data Science and Analytics') {
    //             setDist2([55.4, 4.3, 3.5, 36.8])
    //         } else if (course2 === 'Business Analytics') {
    //             setDist2([34, 20.8, 32.6, 12.6])
    //         } else if (course2 === 'Quantitative Finance') {
    //             setDist2([28.6, 4.9, 18, 48.5])
    //         } else if (course2 === 'Statistics') {
    //             setDist2([34, 6.4, 7.5, 52.1])
    //         } else if (course2 === 'Data Science and Economics') {
    //             setDist2([50, 24.6, 3.3, 22.1])
    //         }
    //     } else if (uni2 === 'NTU') {
    //         if (course2 === 'Data Science and Artificial Intelligence') {
    //             setDist2([46.8, 14.2, 21.8, 17.2])
    //         } else if (course2 === 'Economics and Data Science') {
    //             setDist2([27.8, 34.3, 24, 13.9])
    //         }
    //     } else if (uni2 === 'SMU') {
    //         if (course2 === 'Quantitative Finance') {
    //             setDist2([19.2, 2.6, 60.9, 17.3])
    //         } else if (course2 === 'Data Science and Analytics') {
    //             setDist2([48.4, 14.8, 22.2, 14.5])
    //         } else if (course2 === 'Information Systems (Business Analytics)') {
    //             setDist2([26.7, 32.9, 39.9, 0.5])
    //         }
    //     }
    // }, [])\

    // console.log(distribution1)
    // console.log(distribution2)

    useEffect(() => {
        if (distribution1 && distribution2) {
            const labels = Object.keys(distribution1[0]).slice(2);
            setData1({
                // ['Algorithm & Numerical Methods', 'Machine Learning', 'Project Management', 'Math & Statistics'],
                labels: labels,
                datasets: [
                    {
                        label: `${uni1} ${course1}`,
                        backgroundColor: '#FF5D5D50',
                        borderColor: '#FF5D5D',
                        data:[distribution1[0]['Algorithms and Numerical Methods'], distribution1[0]['Machine Learning'], distribution1[0]['Project Management'], distribution1[0]['Math and Statistics']]
                        // data: dist1
                    },
                    {
                        label: `${uni2} ${course2}`,
                        backgroundColor: '#6792FF50',
                        borderColor: '#6792FF',
                        data:[distribution2[0]['Algorithms and Numerical Methods'], distribution2[0]['Machine Learning'], distribution2[0]['Project Management'], distribution2[0]['Math and Statistics']]
                        // data: dist2
                    }
                ],
            })
        }
    }, [distribution1, distribution2]);
    
    // const data2 = {
    //     labels: ['Finance/Economics', 'Programming/Algorithm', 'Data Analysis/Modelling', 'Statistics'],
    //     datasets: [
    //         {
    //             label: `${uni2} ${course2}`,
    //             backgroundColor: '#6792FF50',
    //             borderColor: '#6792FF',
    //             data:[0.4, 0.2, 0.3, 0.1]
    //         },
    //     ],
    // };

    const options = {
        scale: {
            ticks: {
              display: false,
            }
        },
        legend: {
            position: "bottom",
        }
    };

    return (
         
        <div className="result">
            <div className="chart">
                {data1 && <Radar data={data1} options={options}/>}
            </div>

            {/* <div className="chart">
                <Radar data={data2} options={option}/>
            </div> */}
        </div>
     );
}
 
export default CompareResults;