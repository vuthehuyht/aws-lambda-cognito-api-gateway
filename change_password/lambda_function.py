from signup.utils import ValidateEvent
import boto3

def handler(event, context):
    event = event.get('body')

    data_event = ValidateEvent(event).clean_data()
    if data_event.get("error"):
        return {
            "error": True, 
            "success": False, 
            "message": "Check parameter again"
        }
    event = data_event.get('data')

    client = boto3.client('cognito-idp')

    try:
        response = client.change_password(
            AccessToken=event.get('access_token'),
            PreviousPassword=event.get('old_password'),
            ProposedPassword=event.get('new_password')
        )
        return {
            "error": False, 
            "success": True, 
            "message": "Change password successfully!"
        }
    except client.exceptions.UserNotFoundException:
       return {
            "error": False, 
            "success": True, 
            "message": "Username not found"
        }
    except client.exceptions.InvalidPasswordException:
       return {
            "error": False, 
            "success": True, 
            "message": "Invalid password"
        }
    except client.exceptions.NotAuthorizedException:
       return {
            "error": False, 
            "success": True, 
            "message": "User not authenticate"
        }
    except client.exceptions.UserNotConfirmedException:
       return {
            "error": False, 
            "success": True, 
            "message": "User is not confirmed"
        }
