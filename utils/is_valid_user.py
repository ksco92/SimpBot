from simp_bot import secret_name
from utils.get_secret import get_secret
from utils.run_query import run_query


def is_valid_user(user_nickname):
    """Checks if the nickname of a user is valid."""

    secret = get_secret(secret_name)
    query = """select custom_nickname
               from users
               where custom_nickname = '{}'""".format(user_nickname)
    results = run_query(secret['host'], secret['username'], secret['password'], secret['dbInstanceIdentifier'], query,
                        returns_results=True)

    if len(results) == 1:
        return True
    else:
        return False