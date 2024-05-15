def print_message(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[+] {message}")
            result = func(*args, **kwargs)
            print(f"[-] Finish {message}")
            return result
        return wrapper
    return decorator