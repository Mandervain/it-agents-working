# Outlook Email Not Receiving Messages

Outlook sync failures can result from a corrupted profile, a full mailbox, connection issues to Exchange/Microsoft 365, or a stuck OST cache file.

## Troubleshooting Steps

1. Check Outlook's status bar at the bottom — it should say "Connected to Microsoft Exchange" or "All folders are up to date." If it says "Disconnected" or "Offline," click Send/Receive → Work Offline to toggle back online.
2. Run Send/Receive All Folders (F9) and check for error dialogs.
3. Check mailbox quota: File → Account Settings → select the account → More Settings → Advanced → check the mailbox size. If over 90%, delete or archive items.
4. Repair the Outlook profile: File → Account Settings → Manage Profiles → select the profile → Properties → Email Accounts → Repair.
5. If repair fails, create a new Outlook profile: Control Panel → Mail → Show Profiles → Add. Set it as the default and restart Outlook.
6. As a last resort, delete the OST file (while Outlook is closed): `%localappdata%\Microsoft\Outlook\` — find the `.ost` file for the mailbox and delete it. Outlook will rebuild it on next launch.
7. If emails continue to bounce, the issue may be on the Exchange/M365 server side — escalate to the Exchange administrator with the bounce NDR message body.

## Common Root Causes

- Outlook left in offline mode accidentally
- Full mailbox quota blocking inbound delivery
- Corrupted OST cache
- Exchange transport rule blocking the domain
