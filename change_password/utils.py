class ValidateEvent:
    def __init__(self, event):
        self.event = event

    @staticmethod
    def result(error=True, message="", data=None):
        return {
            "error": error,
            "message": message,
            "data": data
        }

    def clean_data(self):
        if not(self.event.get("access_token") or self.event.get("old_password") or self.event.get("new_password")):
            return self.result(error=True, message="Access token, old password and new password are required.")

        return self.result(data=self.event)
