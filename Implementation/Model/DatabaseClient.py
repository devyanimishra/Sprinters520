from pymongo import MongoClient


class DatabaseClient:

    def __init__(self):
        self.mongoClient = MongoClient('mongodb+srv://root:root@patienttracker.hhhrsal.mongodb.net/PTS?retryWrites=true&w=majority')
        self.db = self.mongoClient['PTS']
