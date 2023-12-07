from azure.cosmos import exceptions, CosmosClient
from config import Cosmos
class database:
    def __init__(self) :
        self.client = CosmosClient(Cosmos.URL, Cosmos.KEY)
        self.database = self.client.get_database_client(Cosmos.DATABASE_NAME)
        self.container = self.database.get_container_client(Cosmos.CONTAINER_NAME_RESUME)
    def check_id_exists(self,id):

        try:
            # Query for the document with the given ID
            query = f"SELECT * FROM c WHERE c.id= '{id}'"
            result = list(self.container.query_items(query, enable_cross_partition_query=True))

            # If any results are returned, the ID exists
            if len(result) > 0:
                return True
            else:
                return False
            
        except exceptions.CosmosResourceNotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    def find_item(self,id):
        query = f"SELECT * FROM c WHERE c.resumeRecord.parsedUserInfo.candidatePersonalInfo.emailAddress[0] = '{id}'"
        items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
        return items[0]

    def check_email_exists(self, email):
        try:
            # Query for the document with the given ID
            query = f"Select * from c where c.resumeRecord.parsedUserInfo.candidatePersonalInfo.emailAddress[0] = '{email}'"
            result = list(self.container.query_items(query, enable_cross_partition_query=True))

            # If any results are returned, the ID exists
            if len(result) > 0:
                return True, result[0]
            else:
                return False, []
            
        except exceptions.CosmosResourceNotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
