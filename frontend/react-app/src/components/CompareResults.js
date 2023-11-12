import 'chart.js/auto';
import { Radar } from 'react-chartjs-2';

const CompareResults = ({uni1, uni2, course1, course2}) => {
    // const metric1 = fetch();
    // const metric2 = fetch();
    
    const data1 = {
        labels: ['Algorithm & Numerical Methods', 'Math & Statistics', 'Project Management', 'Machine Learning'],
        datasets: [
            {
                label: `${uni1} ${course1}`,
                backgroundColor: '#FF5D5D50',
                borderColor: '#FF5D5D',
                data:[0.2, 0.3, 0.1, 0.4]
            },
            {
                label: `${uni2} ${course2}`,
                backgroundColor: '#6792FF50',
                borderColor: '#6792FF',
                data:[0.4, 0.2, 0.3, 0.1]
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