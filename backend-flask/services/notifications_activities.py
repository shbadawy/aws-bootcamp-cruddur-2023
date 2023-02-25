from datetime import datetime, timedelta, timezone
class NotificationsActivities:
  def run():
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now()
    results = [{
    'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
    'handle':  'shimaa Badawy',
    'message': 'Hello world!',
    'created_at': (now - timedelta(days=1)).isoformat(),
    'expires_at': (now + timedelta(days=31)).isoformat()
    }]

    model['data'] = results
    return model