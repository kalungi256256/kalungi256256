import subprocess
import re


def get_profiles():
	try:
		output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], stderr=subprocess.DEVNULL)
		text = output.decode('utf-8', errors='ignore')
	except subprocess.CalledProcessError:
		return []
	profiles = re.findall(r"All User Profile\s*:\s*(.*)", text)
	return [p.strip() for p in profiles]


def get_password(profile):
	try:
		output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], stderr=subprocess.DEVNULL)
		text = output.decode('utf-8', errors='ignore')
	except subprocess.CalledProcessError:
		return None
	m = re.search(r"Key Content\s*:\s*(.*)", text)
	if m:
		return m.group(1).strip()
	return ""


def main():
	profiles = get_profiles()
	print("{:<30} | {:<}".format("Profile", "Password"))
	print("-" * 50)
	for p in profiles:
		pwd = get_password(p)
		if pwd is None:
			pwd = "ERROR"
		print("{:<30} | {:<}".format(p, pwd))
	try:
		input("Press Enter to exit...")
	except EOFError:
		pass


if __name__ == '__main__':
	main()
 