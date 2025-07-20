use retailSalesDB;

db.campaign_feedback.insertMany([
  {
    campaign_name: "Back to School Offer",
    product_name: "Laptop",
    store_name: "Chennai Central",
    feedback: "Offer was great!",
    rating: 4,
    date: new Date("2025-07-01")
  },
  {
    campaign_name: "Summer Sale",
    product_name: "Mouse",
    store_name: "Delhi Mall",
    feedback: "Could be better",
    rating: 3,
    date: new Date("2025-07-01")
  },
  {
    campaign_name: "Festival Bonanza",
    product_name: "Laptop",
    store_name: "Delhi Mall",
    feedback: "Great discount",
    rating: 5,
    date: new Date("2025-07-02")
  }
]);

db.campaign_feedback.createIndex({ campaign_name: 1 });
db.campaign_feedback.createIndex({ product_name: 1 });
db.campaign_feedback.createIndex({ store_name: 1 });
