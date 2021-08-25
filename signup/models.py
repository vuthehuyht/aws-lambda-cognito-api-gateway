import datetime

class ResponseResult():
    _date = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    @staticmethod
    def success(data):
        return {
            'date': ResponseResult._date,
            'result': data
        }

    @staticmethod
    def error(msg):
        return {
            'date': ResponseResult._date,
            'error': {
                'message': msg
            }
        }