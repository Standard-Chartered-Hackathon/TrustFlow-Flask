from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_region = os.getenv("AWS_REGION")
