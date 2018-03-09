from werkzeug.security import safe_str_cmp
from models.user import UserModel

# old
# users = [User(1,'kuro','kuro')]
#
# username_mapping = { u.username : u for u in users}
#
# userid_mapping = { u.id : u for u in users}


def authenticate(username, password):
    # old
    # user = username_mapping.get(username, None)

    # new
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password) :
        return user

def identity(payload):
    user_id = payload['identity']
    # old
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)
