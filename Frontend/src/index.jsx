
import './index.css';
import App from './App';
import 'react-hot-loader/patch';
import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

if (module.hot) {
  module.hot.accept('./App.js', () => {
    mode = 'development'; //add this line here
    const NextRootContainer = require('./App').default;
    render(NextRootContainer);
  });

}

