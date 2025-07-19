DAY 2-MONGODB CRUD OPERATIONS

use companyDB
switched to db companyDB
db
companyDB

CREATE:
db.employees.insertMany([
  {
    name: "Neha Reddy",
    department: "Marketing",
    salary: 45000,
    age: 28
  },
  {
    name: "Faizan Ali",
    department: "Engineering",
    salary: 58000,
    age: 32
  },
  {
    name: "Divya Mehta",
    department: "HR",
    salary: 40000,
    age: 29
  },
  {
    name: "Ravi Verma",
    department: "Sales",
    salary: 35000,
    age: 26
  }
]);

READ

db.employees.find()

db.employees.findOne()

db.employees.findOne({},{name:1,salary:1})

db.employees.find({},{name:1,salary:1})

db.employees.findOne({name:"Amit sharma"})

db.employees.find({salary:{$gt:50000}})

db.employees.find({age:{$gte:28,$lte:32}})

db.employees.find({department:{$in:["HR","Sales"]}})

db.employees.find({department:{$ne:"Marketing"}})

db.employees.find({name:{$regex:"^A"}})

db.employees.find().sort({salary:-1}).limit(3)

UPDATE

db.employees.updateOne({name:"shreya"},{$set:{salary:37000}})

db.employees.updateMany({department:"engineering"},{$inc:{salary:500}})

db.employees.updateMany({department:"Engineering"},{$inc:{salary:500}})

DELETE

db.employees.deleteOne({name:"Divya mehta"})

db.employees.deleteOne({name:"anushka"})

db.employees.deleteMany({department:"Sales"})

