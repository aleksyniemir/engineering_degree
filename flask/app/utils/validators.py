import re

def check_email_regex(email):

    email_regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )   
    if not email_regex.match(email):
        return False
    return True