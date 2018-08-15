import json
import os

FILENAME = 'CustomPerms.json'

DEFAULT_GROUP = {
    'admins': {
        'name': 'admins',
        'members': [],
        'permissions': ['*']
    }
}

def load():
    with open(FILENAME) as f:
        return json.load(f)


def save(data=None):
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            json.dump(DEFAULT_GROUP, f, indent=2)
            print('The default config has been generated!')

    elif data is not None:
        with open(FILENAME, 'w') as f:
            json.dump(data, f, indent=2)
            print('The config has now been saved!')

def add_group(group, permss):
    if group not in perms:
        perms[group] = {'name': group, 'members': [], 'permissions': [permss]}
        save(perms)
        response_ = True
    else:
        response_ = False

    return response_

def del_group(groupp):
    if groupp in perms:
        del perms[groupp]
        response_ = True
        save(perms)
    else:
        response_ = False

    return response_

def add_user_to_group(user, group):
    if group in perms:
        perms[group]['members'].append(user)
        response_ = True
        save(perms)
    else:
        response_ = False

    return response_

def delete_user(user, group):
    if group in perms:
        perms[group]['members'].remove(user)
        response_ = True
        save(perms)
    else:
        response_ = False

    return response_

def add_perm(group, permss):
    if group in perms:
        perms[group]['permissions'].append(permss)
        response_ = True
        save(perms)
    else:
        response_ = False

    return response_

def del_perm(group, permss):
    if group in perms:
        perms[group]['permissions'].remove(permss)
        response_ = True
        save(perms)
    else:
        response_ = False

    return response_

def test_if_user_in_group(user, group):
    if group not in perms:
        permission = 1
    elif user in perms[group]['members']:
        print("WORKING! YAY!")
        permission = perms[group]['permissions']
    else:
        permission = None
        print("not working!")

    return permission

def test_all_groups_for_perm(user, permissions):
    for group in perms.values():
        if user in group['members']:
            if permissions in group['permissions']:
                perms_ = group['permissions']
                print(perms_)
                resp_ = True
                return resp_
        elif user in perms['admins']['members']:
            resp_ = True
            return resp_
    else:
        resp_ = False

    return resp_

save()

perms = load()
