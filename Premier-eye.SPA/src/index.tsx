import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';
// import { configure } from "mobx"
//
// configure({
//     useProxies: "never"
// })

ReactDOM.render(
    <React.StrictMode>
            <App/>
    </React.StrictMode>,
    document.getElementById('root')
);


