from login.utils import Utils
import boto3

CLIENT_ID = '65u3eujpkt97r4p0l9akt28svs'
CLIENT_SECRET = '1gmeivib6vsogc0fupqueigc713rreiaspvsrlbq8ocsuurccuog'


def handler(event, context):
    event = event.get('body')
    print(event)

    client = boto3.client('cognito-idp')

    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': event.get('username'),
                'PASSWORD': event.get('password'),
                'SECRET_HASH': Utils.get_secret_hash(event.get('username'), CLIENT_ID, CLIENT_SECRET)
            }
        )
        print(response)
        if response.get('AuthenticationResult'):
             return {
               "error": False, 
               "success": True, 
               "data": {
                        "id_token": response.get("AuthenticationResult").get("IdToken"),
                        "refresh_token": response.get("AuthenticationResult").get("RefreshToken"),
                        "access_token": response.get("AuthenticationResult").get("AccessToken"),
                        "expires_in": response.get("AuthenticationResult").get("ExpiresIn")
                    }
                }
    except client.exceptions.NotAuthorizedException:
        return {
            "error": False, 
            "success": True, 
            "message": "Username or Password is incorrect"
        }
    except client.exceptions.UserNotConfirmedException:
       return {
            "error": False, 
            "success": True, 
            "message": "User is not confirmed"
        }
    except Exception as e:
        return {
            "error": False, 
            "success": True, 
            "message": str(e)
        }
