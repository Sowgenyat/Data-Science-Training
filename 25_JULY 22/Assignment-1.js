use bookstoreDB
db.books.insertMany([
  { book_id: 1, title: "Power of subconsious mind", author: "Joseph", genre: "self-help", price: 350, stock: 10 },
  { book_id: 2, title: "Atomic Habits", author: "James Clear", genre: "Self-Help", price: 850, stock: 15 },
  { book_id: 3, title: "cpmouter networks", author: "Andrew", genre: "Education", price: 500, stock: 10 },
  { book_id: 4, title: "ponniyin selvan", author: "kalki", genre: "History", price: 300, stock: 25 },
  { book_id: 5, title: "C", author: "Robert", genre: "Programming", price: 600, stock: 8 }
])
db.customers.insertMany([
  { customer_id: 1, name: "Sowgenya", email: "sow@gmail.com", city: "Hyderabad" },
  { customer_id: 2, name: "Anitha", email: "ani@gmail.com", city: "Chennai" },
  { customer_id: 3, name: "Ankit", email: "ankit@gmail.com", city: "Hyderabad" },
  { customer_id: 4, name: "Amitab", email: "amit@gmail.com", city: "Bangalore" },
  { customer_id: 5, name: "Aasha", email: "aasha@gmail.com", city: "Mumbai" }
])
db.orders.insertMany([
  { order_id: 1, customer_id: 1, book_id: 1, order_date: ISODate("2024-07-15T10:30:00Z"), quantity: 2 },
  { order_id: 2, customer_id: 2, book_id: 2, order_date: ISODate("2024-07-20T15:45:00Z"), quantity: 1 },
  { order_id: 3, customer_id: 3, book_id: 3, order_date: ISODate("2024-07-21T11:20:00Z"), quantity: 3 },
  { order_id: 4, customer_id: 4, book_id: 4, order_date: ISODate("2024-07-18T09:00:00Z"), quantity: 1 },
  { order_id: 5, customer_id: 5, book_id: 5, order_date: ISODate("2024-07-19T14:10:00Z"), quantity: 1 }
])

//Basic queries
// 1. Books priced above 500
db.books.find({ price: { $gt: 500 } })

// 2. Customers from Hyderabad
db.customers.find({ city: "Hyderabad" })

// 3. Orders placed after Jan 1, 2023
db.orders.find({ order_date: { $gt: ISODate("2023-01-01T00:00:00Z") } })


//joins via lookup
// 4. Order details with customer name and book title
db.orders.aggregate([
  { $lookup: { from: "customers", localField: "customer_id", foreignField: "customer_id", as: "customer" }},
  { $unwind: "$customer" },
  { $lookup: { from: "books", localField: "book_id", foreignField: "book_id", as: "book" }},
  { $unwind: "$book" },
  { $project: { _id: 0, order_id: 1, customer_name: "$customer.name", book_title: "$book.title", quantity: 1, order_date: 1 }}
])

// 5. Total quantity ordered per book
db.orders.aggregate([
  { $group: { _id: "$book_id", total_quantity: { $sum: "$quantity" }}},
  { $lookup: { from: "books", localField: "_id", foreignField: "book_id", as: "book" }},
  { $unwind: "$book" },
  { $project: { _id: 0, book_title: "$book.title", total_quantity: 1 }}
])

// 6. Number of orders per customer
db.orders.aggregate([
  { $group: { _id: "$customer_id", order_count: { $sum: 1 }}},
  { $lookup: { from: "customers", localField: "_id", foreignField: "customer_id", as: "customer" }},
  { $unwind: "$customer" },
  { $project: { _id: 0, customer_name: "$customer.name", order_count: 1 }}
])


//Aggregate queries
// 7. Total revenue per book
db.orders.aggregate([
  { $lookup: { from: "books", localField: "book_id", foreignField: "book_id", as: "book" }},
  { $unwind: "$book" },
  { $group: { _id: "$book.title", total_revenue: { $sum: { $multiply: ["$quantity", "$book.price"] }}}}
])

// 8. Book with highest total revenue
db.orders.aggregate([
  { $lookup: { from: "books", localField: "book_id", foreignField: "book_id", as: "book" }},
  { $unwind: "$book" },
  { $group: { _id: "$book.title", total_revenue: { $sum: { $multiply: ["$quantity", "$book.price"] }}}},
  { $sort: { total_revenue: -1 }},
  { $limit: 1 }
])

// 9. Total books sold per genre
db.orders.aggregate([
  { $lookup: { from: "books", localField: "book_id", foreignField: "book_id", as: "book" }},
  { $unwind: "$book" },
  { $group: { _id: "$book.genre", total_sold: { $sum: "$quantity" }}}
])

// 10. Customers who ordered more than 2 different books
db.orders.aggregate([
  { $group: { _id: { customer_id: "$customer_id", book_id: "$book_id" }}},
  { $group: { _id: "$_id.customer_id", unique_books: { $sum: 1 }}},
  { $match: { unique_books: { $gt: 2 }}},
  { $lookup: { from: "customers", localField: "_id", foreignField: "customer_id", as: "customer" }},
  { $unwind: "$customer" },
  { $project: { _id: 0, customer_name: "$customer.name", unique_books: 1 }}
])
