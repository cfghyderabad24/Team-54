const express = require('express');
const descapps = express.Router();
const expressAsyncHandler = require('express-async-handler');
require('dotenv').config();

let desc;

descapps.use((req, res, next) => {
    desc = req.app.get('descriptions');
    next();
});

// Example route
descapps.get('/desc', expressAsyncHandler(async (req, res) => {
    const users = await desc.find({}).toArray();
    res.send(users);
}));



module.exports = descapps;
