import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import { DatePicker } from 'antd';
import { Table } from 'antd';
import { MyTable } from "./js/MyTable.js";
import { GCDate } from "./js/MyTable.js";


function App() {
    return (
        <div>
            < MyTable url={url}/>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
