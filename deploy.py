#!/usr/bin/env python3

"""
Run ./deploy.py <number_of_cups>

<number_of_cups> must be between 1 and 9. Over that, the script will only create 9 cups.
If you remove this condition, unexpected behavior can happen, as the port range dedicated to Trackmania servers is 2351-2359.
"""

import sys
import os
import shutil


def main(args: list[str]) -> None:
	# Check arguments validity (1 argument between 1 & 16)
	if len(args) < 2 or not args[1].isdigit():
		print(f"Usage: {args[0]} [number of cups to create]")
		exit(1)

	number_of_cups = int(args[1])

	if not (1 <= number_of_cups <= 16):
		print("[ERROR] Number of cups must be between 1 and 16")
		exit(1)

	# Check which cups we can create
	possible_cups = [i for i in range(1, 17)]
	current_cups = [int(d.replace("cup", "")) for d in os.listdir("compose") if os.path.isdir(os.path.join("compose", d)) and d.startswith("cup")]

	available_cups = list(set(possible_cups) - set(current_cups))

	if not available_cups:
		print("No available cups to create. Exiting.")
		exit(1)

	if len(available_cups) < number_of_cups:
		print(f"Not enough available cups. Will only create {len(available_cups)} cups.")

	# Create the new cups
	count: int = 0
	for i in available_cups:
		if count >= number_of_cups:
			break
		
		# Copy base files 
		cup_dir = os.path.join("compose", f"cup{i}")
		shutil.copytree(os.path.join("compose", "base"), cup_dir)
		os.makedirs(os.path.join(cup_dir, "maps", "MatchSettings"), exist_ok=True)

		# Adapt port and cup name
		with open(os.path.join(cup_dir, "docker-compose.yaml"), "r+") as f:
			content = f.read()
			content = content.replace("$PORT", str(2350 + i))
			content = content.replace("$SERVER_NAME", "InsaLan Cup " + str(i))
			f.seek(0)
			f.write(content)
			f.truncate()
		with open(os.path.join(cup_dir, "cfg_server.xml"), "r+") as f:
			content = f.read()
			content = content.replace("$PORT", str(2350 + i))
			content = content.replace("$SERVER_NAME", "InsaLan Cup " + str(i))
			f.seek(0)
			f.write(content)
			f.truncate()
		count += 1

	print("Cups created successfully. Don't forget to configure them with config.py.")


if __name__ == "__main__":
	main(sys.argv)
