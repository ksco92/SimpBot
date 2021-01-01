import pg8000


def run_query(host, username, password, database, query, returns_results=False, auto_commit=False,
              return_column_names=False):
    conn = pg8000.connect(user=username, password=password, database=database, host=host)
    conn.autocommit = auto_commit
    cursor = conn.cursor()
    cursor.execute(query)
    query_results = []
    column_names = []

    if returns_results:

        if return_column_names:
            for col in cursor.description:
                column_names.append(col[0])

            query_results.append(column_names)

        for row in cursor:
            row = [str(n) if n is not None else '' for n in row]
            query_results.append(list(row))

        conn.close()

        return query_results
    else:
        conn.close()
        return None
