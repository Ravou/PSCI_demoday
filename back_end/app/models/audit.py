from datetime import datetime
from .base import BaseModel

class Audit(BaseModel):
    def __init__(self, target: str, userid: int, consent_type: str, ipaddress: str) :
        self.target = target
        self.userid = userid
        self.consent_type = consent_type
        self.timestamp = datetime.now()
        self.ipaddress = ipaddress
        self.findings = []

    def record_consent(self):
        # Logic to record consent action
        pass

    def revoke_consent(self):
        # Logic to revoke consent action
        pass

    def run_audit(self):
        # Logic to run an audit
        pass

    def log_finding(self, finding: str):
        self.findings.append(finding)
        # Logic to log findings
        pass

    def get_summary(self) -> str:   
        return f"Audit report for {self.target}  {len(self.findings).userid} findings."
        
