import React, { Children } from 'react';
import {createBrowserRouter, RouterProvider} from 'react-router-dom'
import Login from './components/Login/Login';
import MainPage from './components/MainPage.js/MainPage';
import RootLayout from './RootLayout/RootLayout';
import ErrorPage from './components/ErrorPage/ErrorPage';
import DonationPage from './components/DonationPage/DonationPage';
import Receipts from './components/DonationPage/Receipts';


function App() {

  const router = createBrowserRouter([
    {
      path:"",
      element:<RootLayout/>,
      errorElement: <ErrorPage />,
      children:[
        {
          path:"",
          element:<Login/>
        },
        {
          path:"/login",
          element:<Login/>
        },
        {
          path:"/mainpage",
          element:<MainPage/>
        },
        {
          path:"/donationpage",
          element:<DonationPage/>
        },
        {
          path:"/receipts",
          element:<Receipts/>
        }
      ]
    }
  ])

  return (
    <div>
      <RouterProvider router={router}/>
    </div>
  )
}

export default App