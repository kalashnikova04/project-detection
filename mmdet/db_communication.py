import psycopg2


def insert_task(connection, status, worker_id):
    """ Insert a new task into the task's table """

    sql = """INSERT INTO public.main_task(status, worker_id)
             VALUES(%s, %s) RETURNING id;"""

    task_id = None

    try:
        with connection as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (status, worker_id))
                rows = cur.fetchone()
                if rows:
                    task_id = rows[0]

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  
    finally:
        return task_id


def update_task(connection, id, status, worker):
    """ Update task status based on the id """

    sql = """ UPDATE public.main_task
                SET status = %s, worker_id = %s
                WHERE id = %s"""
    
    try:
        with connection as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (status, worker, id))

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
