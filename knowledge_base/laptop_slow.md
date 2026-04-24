# Laptop Performance Degradation

Gradual laptop slowdown is typically caused by high disk usage from Windows Update or antivirus scans, low RAM with too many startup programs, or failing hardware (HDD).

## Troubleshooting Steps

1. Open Task Manager (Ctrl + Shift + Esc) → Performance tab. Note CPU, Memory, and Disk usage. If Disk is at 100%, proceed to step 2.
2. Check for active Windows Update: Settings → Windows Update → pause updates if a large download is in progress. Restart after updates complete.
3. Disable unnecessary startup programs: Task Manager → Startup tab → disable all non-essential items.
4. Run Disk Cleanup: search "Disk Cleanup" → select C: → also run "Clean up system files." Free up space if below 15% free.
5. Check for malware: ensure Windows Defender or the corporate endpoint protection tool is up to date, then run a quick scan.
6. If the disk is an HDD (not SSD), run: `chkdsk C: /f /r` on next restart to check for bad sectors.
7. Increase virtual memory if RAM is consistently above 90%: System Properties → Advanced → Performance Settings → Advanced → Virtual Memory → set to 1.5× installed RAM.
8. If boot time remains above 3 minutes after all the above, capture a Windows Performance Recorder trace and escalate to desktop engineering for hardware evaluation (possible SSD replacement).

## Common Root Causes

- Active Windows Update download/installation
- Bloated startup programs
- Antivirus full scan running in background
- Failing HDD with bad sectors
- Insufficient RAM for workload
