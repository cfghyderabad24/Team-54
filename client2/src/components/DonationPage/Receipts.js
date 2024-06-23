// src/App.js

import React, { useRef } from 'react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import './Receipts.css'; 

const Receipts = () => {
  const invoiceRef = useRef();

  const handleGeneratePdf = async () => {
    const element = invoiceRef.current;
    const canvas = await html2canvas(element);
    const data = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const imgProperties = pdf.getImageProperties(data);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProperties.height * pdfWidth) / imgProperties.width;

    pdf.addImage(data, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save('donation_invoice.pdf');
  };

  const handleSendEmail = () => {
    const email = 'mailto:?subject=Donation Invoice&body=Please find attached the donation invoice.';
    window.open(email);
  };

  // Example invoice details
  const companyName = "Your Charity Organization";
  const fundAmount = "3000";
  const invoiceNumber = "INV-2024-001";
  const date = new Date().toLocaleDateString();

  return (
    <div className="app-container mt-5 rounded-4">
      <div className="invoice" ref={invoiceRef}>
        <h1>Tax Invoice</h1>
        <div className="invoice-details">
          <div><strong>Invoice Number:</strong> {invoiceNumber}</div>
          <div><strong>Date:</strong> {date}</div>
        </div>
        <div className="company-details">
          <div><strong>Company Name:</strong> {companyName}</div>
          <div><strong>Fund Amount:</strong> ₹{fundAmount}</div>
        </div>
        <div className="footer">
          <p>Thank you for your generous donation!</p>
        </div>
      </div>
      <button className='btn me-3' style={{backgroundColor:"#FC6D3F"}} onClick={handleGeneratePdf}>Generate PDF</button>
      <button className='btn' style={{backgroundColor:"#FC6D3F"}} onClick={handleSendEmail}>Send Email</button>
    </div>
  );
};

export default Receipts;