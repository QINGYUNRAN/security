import time

login_attempts = {}
banned_ips = {}


def check_ip_limit(ip_address):
    """
        Checks if an IP address has exceeded the maximum number of login attempts and applies a temporary ban if so.

        Parameters:
        - ip_address (str): The IP address to check.

        Returns:
        - bool: True if the IP is allowed to proceed, False if it has been temporarily banned due to too many attempts.

        Details:
        - Allows up to 5 login attempts within a 10-minute window.
        - If exceeded, the IP address is banned for 30 minutes.
        - Tracks login attempts and enforces temporary bans using in-memory data structures.
    """
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
        banned_ips[ip_address] = current_time + 1800
        return False

    return True