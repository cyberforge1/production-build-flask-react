// frontend/src/App.tsx

import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import StaticPage from './pages/StaticPage/StaticPage';
import FormPage from './pages/FormPage/FormPage';

const App: React.FC = () => {
  return (
    <BrowserRouter basename="/">
      <Routes>
        <Route path="/" element={<StaticPage />} />
        <Route path="/form" element={<FormPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
