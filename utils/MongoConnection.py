from pymongo import MongoClient
from utils.RootSingleton import Singleton


# @Singleton
# class MongoConnnection(object):
#
#     def __init__(self):
#         self.client = MongoClient(host="localhost", port=27017, tz_aware=True, username="goutom", password="123456",
#                              authSource='admin')
#         self.db = self.client.get_database('aggero_fb')
#
#     def get_collection(self, collection_name):
#         return self.db.get_collection(collection_name)
#
#     def close_database(self):
#         self.client.close()


@Singleton
class MongoConnnection(MongoClient):

    def __init__(self):
        super().__init__(host="localhost", port=27017, tz_aware=True, username="goutom", password="123456",
                                  authSource='admin')
        self.db = self.get_database('aggero_fb')

    def get_collection(self, collection_name):
        return self.db.get_collection(collection_name)


