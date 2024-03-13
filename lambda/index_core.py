from index_utils import get_user_info, get_images_from_s3, compare_faces


def lambda_core(event, context):

    user_aid = event['user_aid']
    user_img_url = event['user_img_url']
    user_pid = event['user_pid']

    try:
        aadhaar_img_url, pan_toverify = get_user_info(user_aid)
        if aadhaar_img_url is None:
            return {
                'statusCode': 404,
                'body': 'User not found'
            }

        if user_pid != pan_toverify:
            return {
                'statusCode': 403,
                'body': 'PAN Mismatch'
            }

        aadhaar_img_data, user_img_data = get_images_from_s3(aadhaar_img_url, user_img_url)
        print("getiing imgs from s3")
        if aadhaar_img_data is None or user_img_data is None:
            return {
                'statusCode': 404,
                'body': 'Image not found'
            }

        response = compare_faces(aadhaar_img_data, user_img_data)

        if len(response['FaceMatches']) > 0:
            similarity_score = response['FaceMatches'][0]['Similarity']
            match = True
        else:
            similarity_score = 0
            match = False

        return {
            'statusCode': 200,
            'body': {
                    'match': match,
                    'confidence_score': similarity_score
            }
        }

    except Exception as e:
        print("error ", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }
