# VPN Connectivity Troubleshooting

VPN authentication failures after a password change are the most common cause of VPN disconnections. The VPN client caches credentials and must be updated after any Active Directory password change.

## Troubleshooting Steps

1. Open the VPN client (Cisco AnyConnect / GlobalProtect / FortiClient) and click Disconnect if shown as connected.
2. Clear saved credentials: in the VPN client settings, remove any stored username/password.
3. Re-enter your credentials using your NEW password.
4. If the VPN client prompts for a second factor (MFA), approve it in your Authenticator app.
5. If authentication still fails, open a Command Prompt and run: `ipconfig /flushdns` then retry.
6. Check that the system clock is accurate — Kerberos/certificate auth fails if the clock drifts more than 5 minutes. Run `w32tm /resync` if needed.
7. If the issue persists after all steps above, escalate to the network team with the exact error message from the VPN client logs (Help → Collect Logs).

## Common Root Causes

- Cached old credentials in the VPN client
- MFA token not approved or expired
- DNS cache pointing to stale server IPs
- Active Directory replication delay (password change not yet propagated to all DCs)
