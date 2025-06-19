import sqlite3
from queries import QUERY_LIST, INSERT_STORES

conn = sqlite3.connect('chinook.db')

curs = conn.cursor()

data = [
    ('New York', 'NY', 8, 1, 1),
    ('Los Angeles', 'CA', 11, 0, 1),
    ('Seattle', 'WA', 7, 1, 0),
    ('San Francisco', 'CA', 5, 0, 0)
]

def insert_data_sl(curs, conn, query):
    try:
        curs.executemany(query, data)
        conn.commit()
        return curs.rowcount
    except Exception as e:
        conn.rollback()
        raise Exception(f"Erroc executing insert statement: {e}")

def execute_query_sl(curs, conn, query):
    if query == INSERT_STORES:
        return insert_data_sl(curs, conn, query)
    
    curs.execute(query)
    conn.commit()
    return curs.fetchall()

def execute_queries(curs, conn, queries):
    answers_dict = {}
    for index, query in enumerate(queries):
        answers_dict[index] = execute_query_sl(curs, conn, query)
    return answers_dict

if __name__ == '__main__':
    answers_dict = execute_queries(curs, conn, QUERY_LIST)
    for index, value in enumerate(answers_dict.values()):
        print(f'{index}: {value}')