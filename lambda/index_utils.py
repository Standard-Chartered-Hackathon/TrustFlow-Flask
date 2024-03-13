import pymongo
import boto3
from config import mongoURI, mongo_db_name, mongo_collection_name


def get_user_info(user_id):
    client = pymongo.MongoClient(mongoURI)
    db = client[mongo_db_name]
    collection = db[mongo_collection_name]
    user_data = collection.find_one({"aadhaarCardNo": user_id})

    if user_data:
        user_img_url = user_data.get("aadhaarImageUrl")
        user_pid = user_data.get("panCardNo")
        return user_img_url, user_pid
    else:
        return None, None


def get_images_from_s3(aadhaar_img_url, user_img_url):
    try:
        aadhaar_img_key = '/'.join(aadhaar_img_url.split('/')[3:])
        user_img_key = '/'.join(user_img_url.split('/')[3:])
        s3 = boto3.client('s3')
        aadhaar_img_response = s3.get_object(Bucket='trustflow-aadhaar', Key=aadhaar_img_key)
        aadhaar_img_data = aadhaar_img_response['Body'].read()

        user_img_response = s3.get_object(Bucket='trustflow-user', Key=user_img_key)
        user_img_data = user_img_response['Body'].read()

        return aadhaar_img_data, user_img_data
    except Exception as e:
        print("error ", str(e))
        return None, None


def extract_s3_key(url):
    if not url.startswith('s3://'):
        raise ValueError("Not an S3 URL")
    url = url[5:]
    parts = url.split('/')
    bucket_name = parts[0]
    key_name = '/'.join(parts[1:])
    return bucket_name, key_name


def compare_faces(aadhaar_img_data, user_img_data):
    rekognition = boto3.client('rekognition')
    response = rekognition.compare_faces(
        SourceImage={'Bytes': user_img_data},
        TargetImage={'Bytes': aadhaar_img_data}
    )
    return response
