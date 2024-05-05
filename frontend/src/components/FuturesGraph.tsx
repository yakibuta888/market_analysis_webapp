// import React, { useEffect, useState } from 'react';
// import Plotly from 'plotly.js-basic-dist-min';
// import axios from 'axios';

// const FuturesGraph = () => {
//     const [data, setData] = useState<any[]>([]);

//     useEffect(() => {
//         const fetchData = async () => {
//             const result = await axios.get('/futures-data/gold?trade_dates=2024-04-01');
//             console.log(result.data)
//             setData(result.data);
//         };

//         fetchData();
//     }, []);

//     useEffect(() => {
//         if (data.length > 0) {
//             const trace1 = {
//                 x: data.map(d => d.trade_date),
//                 y: data.map(d => d.settlement_value),
//                 type: 'scatter',
//                 mode: 'lines+markers',
//                 name: 'Settlement Value'
//             };

//             const trace2 = {
//                 x: data.map(d => d.trade_date),
//                 y: data.map(d => d.volume),
//                 yaxis: 'y2',
//                 type: 'bar',
//                 name: 'Volume'
//             };

//             const layout = {
//                 title: 'Futures Data',
//                 yaxis: {title: 'Settlement Value'},
//                 yaxis2: {
//                     title: 'Volume',
//                     overlaying: 'y',
//                     side: 'right'
//                 }
//             };

//             Plotly.newPlot('myDiv', [trace1, trace2], layout);
//         }
//     }, [data]);

//     return <div id="myDiv"></div>;
// };

// export default FuturesGraph;
