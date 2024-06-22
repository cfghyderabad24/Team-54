const express = require('express');
const gencomapanyApp = express.Router();
const expressAsyncHandler = require('express-async-handler');
require('dotenv').config();

let companies;

gencomapanyApp.use((req, res, next) => {
    companies = req.app.get('companies');
    next();
});

// Example route
gencomapanyApp.get('/allusers', expressAsyncHandler(async (req, res) => {
    const users = await companies.find({}).toArray();
    res.send(users);
}));

module.exports = gencomapanyApp;
