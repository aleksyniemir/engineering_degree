from app.utils.validators import check_email_regex  

def test_valid_email():
    valid_emails = [
        "example@example.com",
        "user.name+tag+sorting@example.com",
        "user.name@example.co.in",
        "user_name@example.org",
        "user-name@example.net",
        "1234567890@example.com"
    ]
    for email in valid_emails:
        assert check_email_regex(email) is True

def test_invalid_email():
    invalid_emails = [
        "plainaddress",
        "@no-local-part.com",
        "Outlook Contact <outlook-contact@domain.com>",
        "no-at.domain.com",
        "@no-local-part.com",
        "user name@example.com",
        "user.name@.com.my",
    ]
    for email in invalid_emails:
        assert check_email_regex(email) is False