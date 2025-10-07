import ssl
import socket
import datetime
from urllib.parse import urlparse

def get_certificate_info(url):
    """
    Checks the SSL certificate of any HTTPS URL.
    Returns a dictionary with certificate details or an explicit error message.
    """
    # 1️⃣ Extract hostname from the URL (handles URLs with or without schema)
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if not hostname:
        return {"error": "Invalid URL or hostname not found."}

    context = ssl.create_default_context()

    try:
        # 2️⃣ Create a secure connection on port 443
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # 3️⃣ Extract key certificate information
        subject = dict(x[0] for x in cert.get('subject', []))
        issuer = dict(x[0] for x in cert.get('issuer', []))
        not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')

        return {
            "url": url,
            "hostname": hostname,
            "common_name": subject.get('commonName'),
            "issuer": issuer.get('commonName'),
            "valid_from": not_before.strftime('%Y-%m-%d %H:%M:%S'),
            "valid_until": not_after.strftime('%Y-%m-%d %H:%M:%S'),
            "is_valid_now": not_before <= datetime.datetime.utcnow() <= not_after
        }

    except ssl.SSLError as e:
        return {"url": url, "error": f"SSL Error: {e}"}
    except socket.timeout:
        return {"url": url, "error": "Connection timed out."}
    except socket.gaierror:
        return {"url": url, "error": "Domain name not found."}
    except Exception as e:
        return {"url": url, "error": f"Unknown error: {e}"}


if __name__ == "__main__":
    print("=== Universal SSL Certificate Checker ===\n")

    while True:
        user_input = input("👉 Enter a URL (or type 'exit' to quit): ").strip()
        if user_input.lower() == "exit":
            break

        info = get_certificate_info(user_input)
        print("\nResult:")
        for k, v in info.items():
            print(f"  {k}: {v}")
        print("\n--------------------------------------------\n")

