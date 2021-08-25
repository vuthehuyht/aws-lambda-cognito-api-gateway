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
        if not(self.event.get("username") or self.event.get("email") or self.event.get("password")):
            return self.result(error=True, message="Username, email and password are required.")

        return self.result(data=self.event)
