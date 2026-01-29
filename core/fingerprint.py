def fingerprint(server):
    if not server:
        return "Unknown"

    s = str(server).lower()

    if "apache" in s:
        return "Apache"
    if "nginx" in s:
        return "Nginx"
    if "iis" in s or "microsoft-iis" in s:
        return "IIS"
    if "cloudflare" in s:
        return "Cloudflare"
    if "openresty" in s:
        return "OpenResty"
    if "gunicorn" in s:
        return "Gunicorn"

    return server

