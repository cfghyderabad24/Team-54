import React, { useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { CounterContext } from '../../context/CounterContext';
import { useNavigate } from 'react-router-dom';
import './MainPage.css';
import backgroundpic from '../images/backgroundimage.jpg';

function MainPage() {
  const [selectedDomain, setSelectedDomain] = useState('');
  const [companies, setCompanies] = useState([]);
  const [mailtoLink, setMailtoLink] = useState(null);
  const [desc, setDesc] = useState([]);
  const { user, setUser } = useContext(CounterContext);
  const navigate = useNavigate();

  const handleClick = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate_mailto_link');
      if (response.ok) {
        const data = await response.json();
        setMailtoLink(data.mailto_link);
        window.open(data.mailto_link, '_blank');
      } else {
        alert('Error: ' + response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while generating the email link.');
    }
  };

  useEffect(() => {
    async function fetchCompanies() {
      try {
        const response = await axios.get('http://localhost:3000/gencompany/companies');
        console.log(response.data);
        setCompanies(response.data);
      } catch (error) {
        console.log(error);
      }
    }

    async function fetchDesc() {
      try {
        const response = await axios.get('http://localhost:3000/descapi/desc');
        console.log(response.data);
        setDesc(response.data);
      } catch (error) {
        console.log(error);
      }
    }

    fetchCompanies();
    fetchDesc();
  }, []);

  function logout() {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/');
  }

  const handleSort = (domain) => {
    if (selectedDomain === domain) {
      setSelectedDomain('');
    } else {
      setSelectedDomain(domain);
    }
  };

  const mergedData = companies.map(company => {
    const companyDesc = desc.find(d => d.company_name === company.companyname) || {};
    return { ...company, description: companyDesc.response || 'No description available' };
  });

  const filteredCompanies = selectedDomain
    ? mergedData.filter(company => company.domain.includes(selectedDomain))
    : mergedData;

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      backgroundImage: `url(${backgroundpic})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center calc(50% + 150px)',
      backgroundRepeat: 'no-repeat'
    }}>
      <div>
        {
          user ? (
            <div>
              <nav className='pt-5 flex justify-between'>
                <img className="w-[200px] mx-auto" src="http://jaldhaara.org/wp-content/uploads/2022/04/jaldhaara-logo.png" alt="Logo" />
                <button className='btn text-light position-absolute right-2' onClick={logout} style={{ backgroundColor: "#FC6D3F" }}>Logout</button>
              </nav>
              <div className="main min-h-screen flex flex-col items-center justify-center p-4">
                <h1 className="text-center mb-4 text-2xl font-bold mt-2" style={{ color: '#fb5019' }}>DONOR LEADS</h1>
                <div className="w-full max-w-4xl">
                  <div className="mb-4 text-center">
                    <button
                      className={`btn m-2 ${selectedDomain === 'Water' ? 'btn-dark' : 'btn-outline-dark'}`}
                      onClick={() => handleSort('Water')}
                    >
                      Water
                    </button>
                    <button
                      className={`btn m-2 ${selectedDomain === 'Sanitation' ? 'btn-warning' : 'btn-outline-warning'}`}
                      onClick={() => handleSort('Sanitation')}
                    >
                      Sanitation
                    </button>
                    <button
                      className={`btn m-2 ${selectedDomain === 'Hygiene' ? 'btn-success' : 'btn-outline-success'}`}
                      onClick={() => handleSort('Hygiene')}
                    >
                      Hygiene
                    </button>
                    <button
                      className={`btn m-2 ${selectedDomain === '' ? 'btn-danger' : 'btn-outline-danger'}`}
                      onClick={() => handleSort('')}
                    >
                      All
                    </button>
                  </div>
                  <div className="mb-8">
                    <table className="min-w-full border border-gray-300 rounded-4 shadow-lg m-auto">
                      <thead>
                        <tr className="bg-dark text-white border-b rounded-t-lg">
                          <th className="py-2 px-4 text-left font-semibold">Company Name</th>
                          <th className="py-2 px-4 text-left font-semibold">CSR Spent in Dollars</th>
                          <th className="py-2 px-4 text-left font-semibold">Description</th>
                          <th className="py-2 px-4 text-left font-semibold">Email</th>
                        </tr>
                      </thead>
                      <tbody>
                        {filteredCompanies.map((company, index) => (
                          <tr key={index} className="custom-row">
                            <td className="py-2 px-4 border-b">{company.companyname}</td>
                            <td className="py-2 px-4 border-b">${company.csrspent}</td>
                            <td className="py-2 px-4 border-b">{company.description}</td>
                            <td className="px-4 border-b text-center">
                              <button onClick={handleClick}>Email</button>
                              <i className="fas fa-envelope"></i>
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

export default MainPage;
