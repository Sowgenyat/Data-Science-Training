use attendance_tracker;

db.feedback.insertMany([{employee_id: 1, note: "Handled customer complaints very efficiently", date: ISODate("2025-07-24")},
{employee_id: 1,note: "Needs improvement in punctuality",date: ISODate("2025-07-20")}]);
db.feedback.createIndex({ employee_id: 1 });
