import React from 'react';
import 'assets/main.scss';
import { unstable_HistoryRouter as HistoryRouter, Routes, Route } from 'react-router-dom';
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Queue from 'pages/Events/queue';
import { createBrowserHistory } from 'history';
import Events from 'pages/Events/event';

const history = createBrowserHistory({window});

const App = () => {
  return (
    <HistoryRouter history={history}>
      <Routes>
        <Route path="/" exact Component={Events} />
        <Route path="/queue/:id" exact Component={Queue} />
      </Routes>
      <ToastContainer 
        position="top-center"
        hideProgressBar
        pauseOnFocusLoss={false}
      />
    </HistoryRouter>
  );
};

export default App;