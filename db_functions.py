from models import *

def create_user(username, first_name, user_id):
    us, created = User.get_or_create(username=username, user_id=user_id, defaults={'first_name': first_name})
    return us, created

def create_group(user, group_name, group_id):
    group, created = GroupUsers.get_or_create(user=user, group_id=group_id, defaults={'group_name': group_name})
    return group, created

def create_datashare(url_text, user):
    ds, created = DataSharing.get_or_create(url_text=url_text, user=user)
    return ds, created

def send_required_updates():
    updates = DataSharing.filter(DataSharing.shared==False)