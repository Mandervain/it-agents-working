# Printer Not Printing — Jobs Stuck in Queue

Print jobs queue but do not print when the print spooler is stalled, the driver is corrupted, or the printer has an internal jam/error not shown on the status page.

## Troubleshooting Steps

1. On the affected machine, open the print queue: Start → Devices and Printers → right-click the printer → See what's printing. Cancel all jobs.
2. Restart the Print Spooler service: open Services (services.msc), find "Print Spooler," right-click → Restart.
3. After restarting the spooler, clear the spool directory: navigate to `C:\Windows\System32\spool\PRINTERS\` and delete all files inside (not the folder itself). Then restart the spooler again.
4. Test-print a single page from Notepad to confirm the printer responds.
5. If the printer is shared on a print server, log in to the print server and perform steps 1-3 there as well.
6. Check the printer's physical status: open all trays, confirm no paper jam is present even partially. Power-cycle the printer (hold power button for 10 seconds).
7. If the floor-wide issue persists after spooler restart, the print server may have an outage — escalate to the infrastructure team with the printer's hostname/IP.

## Common Root Causes

- Corrupted or stalled print spooler service
- Stuck large job blocking the queue
- Print server service interruption
- Printer firmware requiring a reboot
