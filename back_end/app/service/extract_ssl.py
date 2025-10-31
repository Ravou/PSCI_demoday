import ssl
import socket
import datetime
from urllib.parse import urlparse
from typing import Dict, Optional, List

class ExtractSSL:
    _certificates: List['ExtractSSL'] = []

    def __init__(self, url: str):
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        self.url = url
        self.parsed_url = urlparse(url)
        self.hostname = self.parsed_url.hostname
        self.context = ssl.create_default_context()
        self.info: Optional[Dict] = None

        # Ajout à la liste globale
        ExtractSSL._certificates.append(self)

        # Récupération automatique du certificat
        self._fetch_certificate()

    def _fetch_certificate(self):
        """Récupère les informations du certificat SSL et les stocke dans self.info"""
        if not self.hostname:
            self.info = {"error": "Invalid URL or hostname not found."}
            return

        try:
            # Connexion sécurisée
            with socket.create_connection((self.hostname, 443), timeout=5) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    cert = ssock.getpeercert()

            # Extraction des informations principales
            subject = dict(x[0] for x in cert.get('subject', []))
            issuer = dict(x[0] for x in cert.get('issuer', []))
            not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
            not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')

            self.info = {
                "url": self.url,
                "hostname": self.hostname,
                "common_name": subject.get('commonName'),
                "issuer": issuer.get('commonName'),
                "valid_from": not_before.strftime('%Y-%m-%d %H:%M:%S'),
                "valid_until": not_after.strftime('%Y-%m-%d %H:%M:%S'),
                "is_valid_now": not_before <= datetime.datetime.utcnow() <= not_after
            }

        except ssl.SSLError as e:
            self.info = {"url": self.url, "error": f"SSL Error: {e}"}
        except socket.timeout:
            self.info = {"url": self.url, "error": "Connection timed out."}
        except socket.gaierror:
            self.info = {"url": self.url, "error": "Domain name not found."}
        except Exception as e:
            self.info = {"url": self.url, "error": f"Unknown error: {e}"}
    
        def __repr__(self):
            return f"ExtractSSL(url='{self.url}', hostname='{self.hostname}')"
