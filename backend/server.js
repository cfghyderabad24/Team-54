const express = require('express');
const app = express();
require('dotenv').config();

const mongoClient = require('mongodb').MongoClient;
const cors = require('cors');
app.use(cors());

const gencomapany = require('./API/gencompany');

app.use(express.json());
const port = process.env.PORT || 8000;

// Connect to DB
mongoClient.connect("mongodb://localhost:27017/")
    .then(client => {
        const targetcompanies = client.db('targetcompanies');
        const companies = targetcompanies.collection('companies');
        app.set('companies', companies);
        console.log("DB connection success");
    })
    .catch(err => console.log("Error in DB connection", err));

// Use the gencomapany router
app.use("/gencomapany", gencomapany);

// Express error handler
app.use((err, req, res, next) => {
    res.send({ message: "error", payload: err.message });
});

// Assign port number
app.listen(port, () => console.log(`Web Server on port ${port}`));
