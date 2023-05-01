from psycopg_pool import ConnectionPool
from flask import current_app as app
import os

def query_wrap_object(template):
  sql = f"""
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  """
  return sql

def query_wrap_array(template):
  sql = f"""
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  """
  return sql

def template(*args):
  pathing = list((app.root_path,'db','sql',) + args)
  pathing[-1] = pathing[-1] + ".sql"

  template_path = os.path.join(*pathing)

  with open(template_path, 'r') as f:
    template_content = f.read()
  return template_content

def query_value(sql,params={}):
    print_sql('value',sql,params)
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql,params)
        json = cur.fetchone()
        return json[0]

connection_url = os.getenv("CONNECTION_URL")

pool = ConnectionPool(connection_url) 
