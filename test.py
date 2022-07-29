from pymongo import MongoClient

client = MongoClient()
db = client.altraheros
dic = {'name':'test'}
posts = db.a1
posts.insert_one(dic)