from django.contrib.auth.models import User,Group

def user_validation(user_details):
    error = {"error": []}
    if user_details['pwd'] != user_details['recheck_pwd']:
        error["error"].append("Password Do Not Match")
    elif User.objects.filter(email=user_details['email']).exists():
        error["error"].append("Email Already Exists!")
    return error
    