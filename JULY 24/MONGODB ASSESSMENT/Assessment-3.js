use jobportalDB

db.jobs.insertMany([{ job_id: 1, title: "Frontend Developer", company: "TechNova", location: "Bangalore", salary: 800000, job_type: "Hybrid", posted_on: new Date("2024-07-10") },
  { job_id: 2, title: "Data Analyst", company: "DataCore", location: "Mumbai", salary: 700000, job_type: "Remote", posted_on: new Date("2024-07-12") },
  { job_id: 3, title: "DevOps Engineer", company: "CloudGen", location: "Hyderabad", salary: 900000, job_type: "On-site", posted_on: new Date("2024-07-08") },
  { job_id: 4, title: "Backend Developer", company: "InnoTech", location: "Chennai", salary: 850000, job_type: "Remote", posted_on: new Date("2024-07-15") },
  { job_id: 5, title: "Product Manager", company: "BuildIt", location: "Delhi", salary: 1200000, job_type: "On-site", posted_on: new Date("2024-07-05") }
]);

db.applicants.insertMany([
  { applicant_id: 1, name: "Sowgenya", skills: ["JavaScript", "MongoDB"], experience: 2, city: "Madurai", applied_on: new Date("2024-07-16") },
  { applicant_id: 2, name: "Ankitha", skills: ["SQL", "Tableau"], experience: 3, city: "Mumbai", applied_on: new Date("2024-07-17") },
  { applicant_id: 3, name: "Poonam", skills: ["Python", "AWS"], experience: 4, city: "Hyderabad", applied_on: new Date("2025-07-14") },
  { applicant_id: 4, name: "Priya ", skills: ["Java", "Spring Boot"], experience: 2, city: "Chennai", applied_on: new Date("2024-07-18") },
  { applicant_id: 5, name: "Sam", skills: ["Agile", "Scrum"], experience: 5, city: "Bangalore", applied_on: new Date("2025-07-13") }
]);

db.applications.insertMany([
  { application_id: 1, applicant_id: 1, job_id: 1, application_status: "Under Review", interview_scheduled: false, feedback: null },
  { application_id: 2, applicant_id: 2, job_id: 2, application_status: "Interview Scheduled", interview_scheduled: true, feedback: "Pending" },
  { application_id: 3, applicant_id: 3, job_id: 3, application_status: "Rejected", interview_scheduled: true, feedback: "Needs more AWS expertise" },
  { application_id: 4, applicant_id: 4, job_id: 4, application_status: "Selected", interview_scheduled: true, feedback: "Excellent Java skills" },
  { application_id: 5, applicant_id: 5, job_id: 5, application_status: "Applied", interview_scheduled: false, feedback: null }
]);



// 1. Find all remote jobs with salary > 10,00,000
db.jobs.find({ job_type: "Remote", salary: { $gt: 1000000 } });

// 2. Get all applicants who know MongoDB
db.applicants.find({ skills: "MongoDB" });

// 3. Number of jobs posted in last 30 days
db.jobs.find({ posted_on: { $gte: new Date(new Date() - 30 * 24 * 60 * 60 * 1000) } }).count();

// 4. List all job applications in ‘interview scheduled’ status
db.applications.find({ interview_scheduled: true });

// 5. Companies that posted more than 2 jobs
db.jobs.aggregate([{ $group: { _id: "$company", job_count: { $sum: 1 } } },{ $match: { job_count: { $gt: 2 } } }]);

// 6. Join applications with jobs to show job title + applicant name
db.applications.aggregate([{$lookup: {from: "jobs",localField: "job_id",foreignField: "job_id",as: "job"}},{ $unwind: "$job" },{$lookup: {from: "applicants",localField: "applicant_id",foreignField: "applicant_id",as: "applicant"}},{ $unwind: "$applicant" },{$project: {_id: 0,applicant_name: "$applicant.name",job_title: "$job.title"}}]);

// 7. Count how many applications each job received
db.applications.aggregate([ { $group: { _id: "$job_id", total_applications: { $sum: 1 } } }]);

// 8. List applicants who applied for more than one job
db.applications.aggregate([{ $group: { _id: "$applicant_id", count: { $sum: 1 } } },{ $match: { count: { $gt: 1 } } },{$lookup: {from: "applicants",localField: "_id",foreignField: "applicant_id",as: "applicant"}},{ $unwind: "$applicant" },{ $project: { _id: 0, applicant_name: "$applicant.name", total_applications: "$count" } }]);

// 9. Top 3 cities with most applicants
db.applicants.aggregate([{ $group: { _id: "$city", count: { $sum: 1 } } },{ $sort: { count: -1 } },{ $limit: 3 }]);

// 10. Average salary per job type
db.jobs.aggregate([{ $group: { _id: "$job_type", avg_salary: { $avg: "$salary" } } }]);

// 11. Update one application status to "offer made"
db.applications.updateOne({ application_status: { $ne: "offer made" } },{ $set: { application_status: "offer made" } });

// 12. Delete job that has no applications
const appliedJobIds = db.applications.distinct("job_id");
db.jobs.deleteMany({_id: { $nin: appliedJobIds }});

// 13. Add "shortlisted": false to all applications
db.applications.updateMany({}, { $set: { shortlisted: false } });

// 14. Increment experience by 1 for applicants from Hyderabad
db.applicants.updateMany({ city: "Hyderabad" },{ $inc: { experience: 1 } });

// 15. Remove applicants who haven’t applied to any job
const appliedIds = db.applications.distinct("applicant_id");
db.applicants.deleteMany({ _id: { $nin: appliedIds }});
