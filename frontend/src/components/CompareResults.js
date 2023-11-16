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
        </div>
     );
}
 
export default CompareResults;