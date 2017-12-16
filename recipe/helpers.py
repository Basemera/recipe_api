def key_is_not_empty(args):
    keys = ('username', 'email', 'password', 'firstname', 'lastname')
    for key in keys:
        if key_is_space(args[key]) == '':
            return True

def key_is_space(string):
    return string.strip()



