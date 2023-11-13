import 'chart.js/auto';
import { useEffect, useState } from 'react';
import { Radar } from 'react-chartjs-2';

const CompareResults = ({uni1, uni2, course1, course2}) => {
    const [distribution1, setDistribution1] = useState(null)
    const [distribution2, setDistribution2] = useState(null)

    useEffect(() => {
        console.log('effect 1 ran')
        fetch(`http://localhost:5000/course-distribution?university=${uni1}&major=${course1}`)
        .then(res => {
            return res.json()
        })
        .then(data => {
            setDistribution1(data)
        });
    }, []);

    useEffect(() => {
        console.log('effect 2 ran')
        fetch(`http://localhost:5000/course-distribution?university=${uni2}&major=${course2}`)
        .then(res => {
            return res.json()
        })
        .then(data => {
            setDistribution2(data)
        });
    }, []);

    

    
    const data1 = {
        labels: ['Algorithm & Numerical Methods', 'Machine Learning', 'Project Management', 'Math & Statistics'],
        datasets: [
            {
                label: `${uni1} ${course1}`,
                backgroundColor: '#FF5D5D50',
                borderColor: '#FF5D5D',
                data:[distribution1['Algorithm & Numerical Methods'], distribution1['Machine Learning'], distribution1['Project Management'], distribution1['Math & Statistics']]
            },
            {
                label: `${uni2} ${course2}`,
                backgroundColor: '#6792FF50',
                borderColor: '#6792FF',
                data:[distribution2['Algorithm & Numerical Methods'], distribution2['Machine Learning'], distribution2['Project Management'], distribution2['Math & Statistics']]
            }
        ],
    };
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
                <Radar data={data1} options={options}/>
            </div>

            {/* <div className="chart">
                <Radar data={data2} options={option}/>
            </div> */}
        </div>
     );
}
 
export default CompareResults;