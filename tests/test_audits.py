from back_end.app.api.audits import Audit

def test_log_and_summary():
    audit = Audit("target", 1, "type", "127.0.0.1")
    audit.log_finding("Finding 1")
    assert "Finding 1" in audit.findings
    assert "Audit summary" in audit.get_summary()

