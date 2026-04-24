# Password Reset and Account Unlock

Account lockouts occur when the incorrect password is entered more than the allowed number of times (default: 5 attempts). Only a helpdesk agent or self-service portal can unlock the account.

## Troubleshooting Steps

1. Direct the user to the Self-Service Password Reset portal at `https://sspr.company.internal` if they have registered their mobile number.
2. If the self-service portal is inaccessible, the helpdesk agent must verify the user's identity using two factors: employee ID and manager name, or security badge number.
3. After identity verification, unlock the account in Active Directory Users and Computers (ADUC): right-click user → Properties → Account → Unlock Account.
4. Force a password reset at next logon: check "User must change password at next logon" in the same dialog.
5. Communicate the temporary password to the user via a pre-agreed out-of-band channel (phone call, not email).
6. Confirm with the user that they can log in and access the required system.
7. Document the unlock action in the ticketing system with the verification method used.

## Security Notes

- Never reset a password based solely on an email request — always verify identity.
- If the lockout appears automated (repeated lockouts in minutes), investigate for credential stuffing and escalate to the security team.
