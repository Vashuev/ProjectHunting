

def login_required(func):
    def inner(*args, **kwargs):
        info = args[2]
        if info.context.user.is_authenticated:
            return func(*args, **kwargs)
        return Exception("No access")
    return inner