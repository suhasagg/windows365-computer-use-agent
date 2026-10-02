# Threat Model
Assets: enterprise credentials, Cloud PC session, screenshots, clipboard, files, browser sessions, command execution, action authority and audit.
Threats: prompt injection on webpages/documents, credential theft, arbitrary navigation, data exfiltration, unsafe commands, approval substitution/replay, UI spoofing, stale coordinates, duplicate submissions, cross-tenant sessions, screenshot leakage and malicious downloads.
Controls: isolated Cloud PC, Entra/Intune/Conditional Access, independent policy gateway, URL allowlists, exact-action approval, DLP, bounded commands, semantic UI inspection, screenshot verification, human takeover, durable audit, short-lived credentials and session teardown.
