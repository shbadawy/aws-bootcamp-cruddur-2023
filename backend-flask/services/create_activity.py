import uuid
from datetime import datetime, timedelta, timezone
from  lib.db import pool

class CreateActivity:
  def run(message, user_handle, ttl, display_name):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'handle':  user_handle,
        'message': message
      }   
    else:
      model['data'] = {
        'uuid': uuid.uuid4(),
        'display_name': display_name,
        'handle':  user_handle,
        'message': message,
        'created_at': now.isoformat(),
        'expires_at': (now + ttl_offset).isoformat()
      }

      sql = f"""
            INSERT INTO public.activities (
            uuid,
            message,
            expires_at
          )
          VALUES (
            (SELECT uuid 
              FROM public.users 
              WHERE users.handle = %(handle)s
              LIMIT 1
            ),
            %(message)s,
            %(expires_at)s
          ) RETURNING uuid;
      """
      
      expires_at = (now + ttl_offset).isoformat()

      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql,{
            'handle': user_handle,
            'message': message,
            'expires_at': expires_at
          })
          # this will return a tuple
          # the first field being the data
          results = cur.fetchone()
          # print('#######')
          # print(results)
    return model 