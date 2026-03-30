import subprocess
import re
import platform


def get_profiles():
	os_sys = platform.system()
	if os_sys == "Windows":
		try:
			output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], stderr=subprocess.DEVNULL)
			text = output.decode('utf-8', errors='ignore')
		except subprocess.CalledProcessError:
			return []
		profiles = re.findall(r"All User Profile\s*:\s*(.*)", text)
		return [p.strip() for p in profiles]
	elif os_sys == "Linux":
		try:
			output = subprocess.check_output(['nmcli', '-t', '-f', 'TYPE,NAME', 'connection', 'show'], stderr=subprocess.DEVNULL)
			text = output.decode('utf-8', errors='ignore')
			profiles = []
			for line in text.split('\n'):
				if line.startswith('802-11-wireless:'):
					profiles.append(line.split(':', 1)[1])
			return profiles
		except (subprocess.CalledProcessError, FileNotFoundError):
			return []
	return []


def get_password(profile):
	os_sys = platform.system()
	if os_sys == "Windows":
		try:
			output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], stderr=subprocess.DEVNULL)
			text = output.decode('utf-8', errors='ignore')
		except subprocess.CalledProcessError:
			return None
		m = re.search(r"Key Content\s*:\s*(.*)", text)
		if m:
			return m.group(1).strip()
		return ""
	elif os_sys == "Linux":
		try:
			output = subprocess.check_output(['nmcli', '-s', '-g', '802-11-wireless-security.psk', 'connection', 'show', profile], stderr=subprocess.DEVNULL)
			return output.decode('utf-8', errors='ignore').strip()
		except (subprocess.CalledProcessError, FileNotFoundError):
			return None
	return None


def scan_networks():
	os_sys = platform.system()
	if os_sys == "Windows":
		try:
			output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks'], stderr=subprocess.DEVNULL)
			text = output.decode('utf-8', errors='ignore')
			networks = re.findall(r"SSID \d+ : (.*)", text)
			return [n.strip() for n in networks if n.strip()]
		except subprocess.CalledProcessError:
			return []
	elif os_sys == "Linux":
		try:
			output = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stderr=subprocess.DEVNULL)
			text = output.decode('utf-8', errors='ignore')
			return [line.strip() for line in text.split('\n') if line.strip()]
		except (subprocess.CalledProcessError, FileNotFoundError):
			return []
	return []


def anonymous():
	print("\nScanning for available networks...")
	networks = scan_networks()
	unique_networks = sorted(list(set(networks)))
	print("\n{:<30} | {:<}".format("Available Network", "Password"))
	print("-" * 50)
	for net in unique_networks:
		pwd = get_password(net)
		if pwd:
			print("{:<30} | {:<}".format(net, pwd))
		else:
			print("{:<30} | {:<}".format(net, "N/A"))


def main():
	print("1. List all saved profiles")
	print("2. Scan available networks (Anonymous)")
	choice = input("Enter choice (1/2): ").strip()
	if choice == '2':
		anonymous()
	else:
		profiles = get_profiles()
		print("\n{:<30} | {:<}".format("Profile", "Password"))
		print("-" * 50)
		for p in profiles:
			pwd = get_password(p)
			if pwd is None:
				pwd = "ERROR"
			print("{:<30} | {:<}".format(p, pwd))
	try:
		input("\nPress Enter to exit...")
	except EOFError:
		pass


if __name__ == '__main__':
	main()
 