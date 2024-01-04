from pymongo import MongoClient
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# MongoDB server connection string
MONGODB_CONNECTION_STRING = "***********************"

#First include this:
    # In the terminal pip install django-cors-headers
    # In settings.py, add 'corsheaders' to the INSTALLED_APPS list:
# INSTALLED_APPS = [
#     # ...
#     'corsheaders', #Add this
#     # ...
# ]


    # In settings.py  also  Add 'corsheaders.middleware.CorsMiddleware' to the MIDDLEWARE list :
# MIDDLEWARE = [
#     # ...
#     'corsheaders.middleware.CorsMiddleware',  #Add this
#     # Make sure it's before Django's CommonMiddleware
#     'django.middleware.common.CommonMiddleware', #Add this
#     # ...
# ]


    # Still In settings.py  Add this line alone :
# CORS_ALLOW_ALL_ORIGINS = True


# SIGN UP FUNCTION.
# SAVES THE NAME AND PHONE NUMBER ENTERED FOR A CLIENT

@csrf_exempt
def save_data(request):
    # Define the database and the collection name
    DB_NAME = "learner"
    COLLECTION_NAME = "trial"

    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            phone = data.get('phone')

            if name and phone:
                client = MongoClient(MONGODB_CONNECTION_STRING)
                db = client[DB_NAME]
                collection = db[COLLECTION_NAME]

                # Prepare user data
                user_data = {
                    'name': name,
                    'phone': phone
                }

                # Insert the data into the collection
                collection.insert_one(user_data)

                client.close()  # Close the MongoDB connection

                # Return success response
                return JsonResponse({'message': 'Contact saved successfully'}, status=200)
            else:
                return JsonResponse({'message': 'Name and phone number are required'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
