import time

login_attempts = {}
banned_ips = {}


def check_ip_limit(ip_address):
    current_time = time.time()
    if ip_address in banned_ips:
        if current_time < banned_ips[ip_address]:
            return False
        else:
            del banned_ips[ip_address]

    attempts = login_attempts.get(ip_address, [])
    attempts = [ts for ts in attempts if current_time - ts <= 600]
    attempts.append(current_time)
    login_attempts[ip_address] = attempts

    if len(attempts) > 5:
        banned_ips[ip_address] = current_time + 1800  # 禁止30分钟
        return False

    return True