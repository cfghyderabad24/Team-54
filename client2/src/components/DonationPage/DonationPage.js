// import React from 'react'
// import { useContext } from 'react'
// import { CounterContext } from '../../context/CounterContext'
// import { useNavigate } from 'react-router-dom'

// function MainPage() {

//   const {user,setUser} = useContext(CounterContext)

//   const navigate = useNavigate()
  

//   function logout(){
//     setUser(null)
//     localStorage.removeItem('token')
//     localStorage.removeItem('user')
//     navigate("/")
//   }


//   return (
//     <div>
//       {
//         user ? <h1>Welcome {user.username}</h1> : <h1>Please Login</h1>
//       }
//       <button onClick={logout} >Logout</button>
//     </div>
//   )
// }

// export default MainPage
import React, { useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { CounterContext } from '../../context/CounterContext';
import { useNavigate } from 'react-router-dom';
import backgroundpic from '../images/backgroundimage.jpg';

function DonationPage() {
  const [selectedDomain, setSelectedDomain] = useState('');
  

  const { user, setUser } = useContext(CounterContext);
  const navigate = useNavigate();

  const companies  = [
    {
      "companyName": "Tech Innovators Inc.",
      "donations": 50000
    },
    {
      "companyName": "Green Energy Solutions",
      "donations": 75000
    },
    {
      "companyName": "Healthcare Heroes Ltd.",
      "donations": 120000
    },
    {
      "companyName": "Future Finance Corp.",
      "donations": 30000
    },
    {
      "companyName": "Education Excellence",
      "donations": 45000
    },
    {
      "companyName": "Food For All",
      "donations": 80000
    },
    {
      "companyName": "Clean Water Initiative",
      "donations": 95000
    },
    {
      "companyName": "Tech For Good",
      "donations": 62000
    },
    {
      "companyName": "Global Health Org",
      "donations": 110000
    },
    {
      "companyName": "Future Builders",
      "donations": 54000
    }
  ]
  

  
  function logout(){
    setUser(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate("/")
  }

  const handleSort = (domain) => {
    if(selectedDomain === domain) {
      setSelectedDomain('');
    }
    else{
      setSelectedDomain(domain);
    }
  };

  const filteredCompanies = selectedDomain
    ? companies.filter(company => company.domain.includes(selectedDomain))
    : companies;

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      backgroundImage: `url(${backgroundpic})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center calc(50% + 150px)', // Align the background image to the bottom
      backgroundRepeat: 'no-repeat'
    }}>
    <div>
      {
        user ? (
          <div>
            <nav className=' pt-5 flex justify-between '>
            <img  className="w-[200px] mx-auto " src="http://jaldhaara.org/wp-content/uploads/2022/04/jaldhaara-logo.png"  alt="Logo" />
            <button className='btn text-light position-absolute right-2' onClick={logout} style={{backgroundColor:"#FC6D3F"}}>Logout</button>
            </nav>
          <div className="main min-h-screen flex flex-col items-center justify-center p-4">

            {/* Logo at the top left */}
            
      
            <h1 className="text-center mb-4 text-2xl font-bold mt-2" style={{ color: '#fb5019' }}>Donations Received</h1>
            <div className="w-full max-w-4xl">
              
              <div className="overflow-x-auto mb-8 rounded-4">
                <table className="min-w-full border border-gray-300 rounded-lg shadow-lg m-auto">
                  <thead className=''>
                    <tr className="bg-dark text-white border-b rounded-t-lg">
                      <th className="py-2 px-4 text-left font-semibold">Company Name</th>
                      <th className="py-2 px-4 text-left font-semibold">CSR Spent in Rs</th>
                      <th className="py-2 px-4 text-left font-semibold">Receipt</th>
                    </tr>
                  </thead>
                  <tbody  >
                    {filteredCompanies.map((company, index) => (
                      <tr key={index} className="custom-row">
                        <td className="py-2 px-4 border-b">{company.companyName}</td>
                        <td className="py-2 px-4 border-b">{company.donations}</td>
                        <td className="px-4 border-b  text-center">
                            <button className='btn text-white mt-1 mb-1' onClick={()=>navigate('/receipts')} style={{backgroundColor:"#FC6D3F"}}>Receipt</button>                          
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              
            </div>
          </div> 
          </div>
        ) : (
          <div className='m-auto flex items-center justify-center min-h-screen'>
            <div>
              <h5>Unauthorized access, Please login</h5>
              <button className='d-block m-auto btn' onClick={() => navigate('/login')} style={{ backgroundColor: "#FC6D3F" }}>Login</button>
            </div>
          </div>
        )
      }
    </div>
    </div>
  );
}

export default DonationPage;
