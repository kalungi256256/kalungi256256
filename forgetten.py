# Save as "router_password_retriever.py"
import subprocess

def get_router_password(ip: str, username: str = "admin"):
    """Retrieve password for YOUR OWN router (if saved locally)"""
    try:
        # For Windows (if you've connected via browser)
        cmd = f'powershell "Get-Credential -UserName {username} | Export-Clixml \'.\\{ip}.xml\'"'
        subprocess.run(cmd, shell=True, check=True)
        
        return f"Password saved to {ip}.xml (open with PowerShell: Import-Clixml)"
    
    except Exception as e:
        return f"Manual recovery needed: Log into {ip} as {username} → Wireless Settings"

# Usage example (for YOUR router at 192.168.1.1)
print(get_router_password("192.168.1.1"))
