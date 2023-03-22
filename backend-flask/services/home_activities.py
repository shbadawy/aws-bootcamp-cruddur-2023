from datetime import datetime, timedelta, timezone
from lib.db import pool, query_wrap_array
from opentelemetry import trace
import os


tracer = trace.get_tracer("Home tracer")

class HomeActivities:
  def run():
    #logger.info("Home activities")
    with tracer.start_as_current_span("Show home activities"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()
      span.set_attribute("app.now", now.isoformat())

      sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities 
      LEFT JOIN public.users ON users.uuid = activities.uuid
      ORDER BY activities.created_at DESC
      """)

      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          results = cur.fetchall()

      span.set_attribute("app.result_length", len(results))
      return results[0][0]