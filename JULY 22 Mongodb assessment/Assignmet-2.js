use moviestreamdb
db.users.insertMany([
  { user_id: 1, name: "Sowgenya", email: "sowgenya265@gmail.com", country: "India" },
  { user_id: 2, name: "Anitha", email: "ani@gmail.com", country: "UK" },
  { user_id: 3, name: "Ankit", email: "ankit@gmail.com", country: "India" },
  { user_id: 4, name: "David", email: "david@gmail.com", country: "USA" },
  { user_id: 5, name: "Emily", email: "emi@.gmail.com", country: "Japan" }
])

db.movies.insertMany([
  { movie_id: 1, title: "Life of pi", genre: "Biography", release_year: 2010, duration: 148 },
  { movie_id: 2, title: "The Dark Knight", genre: "Action", release_year: 2008, duration: 152 },
  { movie_id: 3, title: "Dark blue sea", genre: "Thriller", release_year: 2019, duration: 132 },
  { movie_id: 4, title: "Enchanted", genre: "Fantasy", release_year: 1998, duration: 169 },
  { movie_id: 5, title: "Beauty and beast", genre: "Drama", release_year: 2019, duration: 122 },
  { movie_id: 6, title: "Frozen2", genre: "Animation", release_year: 1995, duration: 81 }
])

db.watch_history.insertMany([
  { watch_id: 1, user_id: 1, movie_id: 1, watched_on: ISODate("2023-06-10"), watch_time: 148 },
  { watch_id: 2, user_id: 2, movie_id: 3, watched_on: ISODate("2023-07-01"), watch_time: 132 },
  { watch_id: 3, user_id: 3, movie_id: 2, watched_on: ISODate("2023-07-15"), watch_time: 152 },
  { watch_id: 4, user_id: 1, movie_id: 4, watched_on: ISODate("2023-07-20"), watch_time: 169 },
  { watch_id: 5, user_id: 2, movie_id: 1, watched_on: ISODate("2023-07-21"), watch_time: 148 },
  { watch_id: 6, user_id: 4, movie_id: 5, watched_on: ISODate("2023-07-22"), watch_time: 122 },
  { watch_id: 7, user_id: 5, movie_id: 6, watched_on: ISODate("2023-07-22"), watch_time: 81 },
  { watch_id: 8, user_id: 2, movie_id: 11, watched_on: ISODate("2023-07-23"), watch_time: 148 } 
])


//Basic Queries
//1. Find all movies with duration > 100 minutes
db.movies.find({duration:{$gt:100}})

//2. List users from 'India'
db.users.find({country:"India"})

//3. Get all movies released after 2020
db.movies.find({released_year:{$gt:2020}})

//intermediate queries

//4.show full watch history
db.watch_history.aggregate([{$lookup: {from: "users",localField: "user_id",foreignField: "user_id",as: "user"}},{ $unwind: "$user" },{$lookup: {from: "movies",localField: "movie_id",foreignField: "movie_id",as: "movie"}},{ $unwind: "$movie" },{$project: {_id: 0,user_name: "$user.name",movie_title: "$movie.title",watch_time: 1}}])

//5. List each genre and number of times movies in that genre were watched
db.watch_history.aggregate([{$lookup: {from: "movies",localField: "movie_id",foreignField: "movie_id",as: "movie"}},{ $unwind: "$movie" },{$group: {_id: "$movie.genre",watch_count: { $sum: 1 }}},{$project: {genre: "$_id",watch_count: 1,_id: 0 }}])

//6Display total watch time per user
db.watch_history.aggregate([{ $group: {_id: "$user_id",total_watch_time: { $sum: "$watch_time" }}},{$lookup: {from: "users",localField: "_id",foreignField: "user_id", as: "user" }},{ $unwind: "$user" },{$project: { _id: 0,user_name: "$user.name",total_watch_time: 1 }}])




//Advanced:
//7. Find which movie has been watched the most (by count).
db.watch_history.aggregate([{ $group: {_id: "$movie_id",watch_count: { $sum: 1 }}},{ $sort: { watch_count: -1 } },{ $limit: 1 },{$lookup: {from: "movies",localField: "_id",foreignField: "movie_id",as: "movie"}},{ $unwind: "$movie" },{$project: {_id: 0,movie_title: "$movie.title",watch_count: 1}}])

//8. Identify users who have watched more than 2 movies.
db.watch_history.aggregate([{$group: {_id: "$user_id",unique_movies: { $addToSet: "$movie_id" }}},{$project: {movie_count: { $size: "$unique_movies" }}},{ $match: { movie_count: { $gt: 2 } } },{$lookup: {from: "users",localField: "_id",foreignField: "user_id",as: "user"}},{ $unwind: "$user" },{$project: {_id: 0,user_name: "$user.name",movie_count: 1}}])

//9. Show users who watched the same movie more than once.
db.watch_history.aggregate([{$group: {_id: { user_id: "$user_id", movie_id: "$movie_id" },watch_count: { $sum: 1 }}},{ $match: { watch_count: { $gt: 1 } } },{$lookup: {from: "users",localField: "_id.user_id",foreignField: "user_id",as: "user"}},{ $unwind: "$user" },{$lookup: {from: "movies",localField: "_id.movie_id",foreignField: "movie_id",as: "movie"}},{ $unwind: "$movie" },{$project: {_id: 0,user_name: "$user.name",movie_title: "$movie.title",watch_count: 1}}])

//10. Calculate percentage of each movie watched compared to its full duration
( watch_time/duration * 100 ).

db.watch_history.aggregate([{$lookup: {from: "movies",localField: "movie_id",foreignField: "movie_id",as: "movie"}},{ $unwind: "$movie" },{$project: {_id: 0,user_id: 1,movie_title: "$movie.title",watch_time: 1,duration: "$movie.duration",percentage_watched: {$round: [{ $multiply: [{ $divide: ["$watch_time", "$movie.duration"] }, 100] },2]}}}])












