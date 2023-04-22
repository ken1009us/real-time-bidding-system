def authenticate_user(username, password):
    with open('auth.txt', 'r') as file:
        for line in file:
            user, pwd = line.strip().split(',')
            if username == user and password == pwd:
                return True

    return False
