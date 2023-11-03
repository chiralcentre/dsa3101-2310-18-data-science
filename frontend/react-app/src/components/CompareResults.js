import 'chart.js/auto';
import { Radar } from 'react-chartjs-2';

const CompareResults = ({uni1, uni2, course1, course2}) => {
    // const metric1 = fetch();
    // const metric2 = fetch();
    
    const data1 = {
        labels: ['Finance/Economics', 'Programming/Algorithm', 'Data Analysis/Modelling', 'Statistics'],
        datasets: [
            {
                label: `${uni1} ${course1}`,
                backgroundColor: 'red',
                borderColor: 'black',
                data:[0.2, 0.3, 0.1, 0.4]
            },
        ],
    };
    const data2 = {
        labels: ['Finance/Economics', 'Programming/Algorithm', 'Data Analysis/Modelling', 'Statistics'],
        datasets: [
            {
                label: `${uni2} ${course2}`,
                backgroundColor: 'blue',
                borderColor: 'black',
                data:[0.5, 0.1, 0.3, 0.1]
            },
        ],
    };

    const option = {

    };

    return ( 
        <div className="result">
            <div className="chart">
                <Radar data={data1} options={option}/>
            </div>

            <div className="chart">
                <Radar data={data2} options={option}/>
            </div>
        </div>
     );
}
 
export default CompareResults;