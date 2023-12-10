import hashlib
from datetime import datetime,timedelta
from azure.cosmos import CosmosClient
from config import  Cosmos
import json

client = CosmosClient(Cosmos.URL, Cosmos.KEY)
database = client.get_database_client(Cosmos.DATABASE_NAME)
container = database.get_container_client(Cosmos.CONTAINER_NAME)

def generate_data(email_id,mobile,name,workauth,annualrate,hourlyrate,relocate,location):
    
    sha1_hash = hashlib.sha1(email_id.encode()).hexdigest()
    name_parts = name[0].split()
    if len(name_parts) == 1:
        first_name = name_parts[0]
        last_name = None
        middle_name = None
    if len(name_parts) == 2:
        first_name = name_parts[0]
        last_name = name_parts[-1]
        middle_name = None
    if len(name_parts) > 2:
        first_name = name_parts[0]
        last_name = name_parts[-1]
        middle_name = " ".join(name_parts[1:-1])

    current_date = datetime.today()
    data = {
    "parsedUserInfo": {
        "eximiusId": sha1_hash,
        "candidatePersonalInfo": {
            "contactNumber": {
                "phone": {
                    "mobile": str(mobile)
                }
            },
            "candidateFullName": {
                "firstName": str(first_name),
                "middleName": str(middle_name) if middle_name else None,
                "lastName": str(last_name) if last_name else None
            },
            "emailAddress": [email_id]
        }
    },
    "additionalParameters": {
        "jobWorkAuthorization": str(workauth),
        "packageRate": {
            "annual_rate": int(annualrate),
            "hourly_rate": int(hourlyrate)
        },
        "willingToRelocate": str(relocate),
        "location": str(location),
        "lastUpdated": (current_date - timedelta(days=9)).strftime("%Y-%m-%d")
    }
}    
    try:
        data['id'] = email_id
        container.upsert_item(data)
        return 1
    except Exception:
        return 0 