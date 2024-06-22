const exp = require('express');
const app=exp()
require('dotenv').config()

const mongoClient = require('mongodb').MongoClient;
const cors = require('cors')
app.use(cors())


const userapi =require('./API/userapi')


app.use(exp.json())
const port = process.env.PORT || 8000




//connect to DB
mongoClient.connect(process.env.MONGO_URI)
.then(client=>{
    const targetcompanies = client.db('targetcompanies')

    const companies = targetcompanies.collection('companies')


    app.set('companies',companies)

    
    console.log("DB connection success")
})
.catch(err=>console.log("err in DB connection",err))



app.use("/userapi", userapi)


//express error handler
app.use((err,req,res,nest)=>{
    res.send({message:"error",payload:err.message})
})

//assign port no.
app.listen(port,()=>console.log(`Web Server on port ${port}`))