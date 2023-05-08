from psycopg_pool import ConnectionPool
from flask import current_app as app
import os

def print_sql(self,title,sql,params={}):
  cyan = '\033[96m'
  no_color = '\033[0m'
  print(f'{cyan} SQL STATEMENT-[{title}]------{no_color}')
  print(sql,params)

def query_array_json(sql,params={}):
  print_sql('array',sql,params)

  wrapped_sql = query_wrap_array(sql)
  with pool.connection() as conn:
    with conn.cursor() as cur:
      cur.execute(wrapped_sql,params)
      json = cur.fetchone()
      return json[0]

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

def query_commit(self,sql,params={}):
  self.print_sql('commit with returning',sql,params)

  pattern = r"\bRETURNING\b"
  is_returning_id = re.search(pattern, sql)

connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url) 
