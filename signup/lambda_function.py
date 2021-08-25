from signup.models import ResponseResult
from signup.utils import ValidateEvent
import boto3
import hmac
import base64
import hashlib
import logging

USER_POOL_ID = ''
CLIENT_ID = '65u3eujpkt97r4p0l9akt28svs'
CLIENT_SECRET = '1gmeivib6vsogc0fupqueigc713rreiaspvsrlbq8ocsuurccuog'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
   # Validate event
#    data_event = ValidateEvent(event.get('body')).clean_data()

#    if data_event.get('error'):
#        return ResponseResult.error(data_event.get('message'))
   event = event.get('body')

   logger.info(f'Event: {event}')

   client = boto3.client('cognito-idp')
   try:
       response = client.sign_up(
           ClientId=CLIENT_ID,
           SecretHash=get_secret_hash(event.get('username')),
           Username=event.get('username'),
           Password=event.get('password'),
           UserAttributes=[
               {
                   'Name': 'email',
                   'Value': event.get('email')
               }
           ],
           ValidationData=[
                {
                    'Name': "email",
                    'Value': event.get('email')
                },
                {
                    'Name': "custom:username",
                    'Value': event.get('username')
                }
           ]
       )
   except client.exceptions.UsernameExistsException as e:
        return {
            "error": False, 
            "success": True, 
            "message": "This username already exists", 
            "data": None
        }
   except client.exceptions.InvalidPasswordException as e:
        return {
            "error": False, 
            "success": True, 
            "message": "Password should have Caps, Special chars, Numbers", 
            "data": None
        }
   except client.exceptions.UserLambdaValidationException as e:
        return {
               "error": False, 
               "success": True, 
               "message": "Email already exists", 
               "data": None
            }
    
   except Exception as e:
        logger.error(e)
        return {
            "error": False, 
            "success": True, 
            "message": str(e), 
            "data": None
        }
    
   return {
       "error": False, 
        "success": True, 
        "message": "Your account is created successfully", 
        "data": None
    }


def get_secret_hash(username):
    msg = str(username) + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
