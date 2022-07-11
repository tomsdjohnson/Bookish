import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './components/App';
import {Button} from "reactstrap";
import TestButton from "./components/Button";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
      <TestButton />
  </React.StrictMode>
);
