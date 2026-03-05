#!/usr/bin/env python3

"""
Run ./config.py

This script configures server instances with the selected configuration (stored in config.json), map pool (stored in compose/maps) and map order.
"""

import xml.etree.ElementTree as etree
import json
import os
import xml.dom.minidom


def selector(pool: list[str], q_str: str, a_str: str, unique_choice: bool = True, all_choice: bool = False) -> str | list[str]:
	"""
	A generic selector asking the user to select one or multiple options.
	If multiple choices are allowed, they haave to be separated by spaces.

	:param pool: a dict associating a unique index with an option
	:param q_str: the text that will be printed before displaying options
	:param a_str: the text that will be printed to ask for user input
	:param unique_choice: whether the choice is a unique value or an ordered list of values
	"""
	options = sorted(pool)
	print(q_str)
	for i, key in enumerate(options):
		print(f"	{i + 1} - {key}")
	if all_choice:
		print(f"	999 - all")
	choices = input(a_str).strip().split()
	if unique_choice and len(choices) > 1:
		print("Only one choice is allowed. Exiting.")
		exit(1)
	res = []
	for choice in choices:
		if choice in options:
			res.append(choice)
		elif choice.isdigit():
			if all_choice and int(choice) == 999:
				res = options
			elif 0 < int(choice) <= len(options):
				res.append(options[int(choice) - 1])
		else:
			print(f"Choice '{choice}' not found. Exiting.")
			exit(1)
	if unique_choice:
		return res[0]
	return res


def to_tm_val(value: bool | int | list) -> str:
	"""
	Converts a Python value to its Trackmania setting representation.

	:param value: the Python value to convert
	:return: the Trackmania string representation of the value
	"""
	if isinstance(value, bool):
		return "1" if value else "0"
	if isinstance(value, list):
		return ",".join(str(i) for i in value)
	return str(value)


def handle_gameinfo(parent: etree.Element, data: dict) -> None:
	"""
	Handles the gameinfo section of the configuration.

	:param parent: the parent XML element to which the gameinfos element will be added
	:param data: the dictionary containing gameinfo settings
	"""
	game_infos = etree.SubElement(parent, "gameinfos")
	for k, v in data.items():
		if isinstance(v, dict):
			sibling = etree.SubElement(parent, k)
			for sub_k, sub_v in v.items():
				etree.SubElement(sibling, sub_k).text = to_tm_val(sub_v)
		else:
			etree.SubElement(game_infos, k).text = to_tm_val(v)


def handle_script_settings(parent: etree.Element, data: dict) -> None:
	"""
	Handles the script_settings section of the configuration.

	:param parent: the parent XML element to which the script_settings element will be added
	:param data: the dictionary containing script settings
	"""
	script_settings = etree.SubElement(parent, "script_settings")
	for k, v in data.items():
		setting = etree.SubElement(script_settings, "setting")
		setting.set("name", k)
		if isinstance(v, bool):
			setting.set("type", "boolean")
		elif isinstance(v, int):
			setting.set("type", "integer")
		else:
			setting.set("type", "string")
		setting.set("value", to_tm_val(v))


def main() -> None:
	"""
	Creates and apply the configuration to server instances.
	"""
	# List and select cups
	cup_directories = [d for d in os.listdir("compose") if "cup" in d]
	if not cup_directories:
		print("No cup to apply the configuration to. Exiting.")
		exit(1)
	selected_cups = selector(
		cup_directories,
		f"Available cups:",
		"Enter the cups names or indexes separated by spaces: ",
		unique_choice=False,
		all_choice=True
	)

	# List and select configuration
	settings = json.load(open("config.json", "r"))
	config_name = str(selector(
		[str(k) for k in settings.keys()],
		"Available configurations in config.json:",
		"Enter the configuration name or index: "
	))

	# List and select map pool
	map_pools: list[str] = os.listdir(os.path.join("compose","maps"))
	map_pool = selector(
		map_pools,
		"Available map pools in compose/maps:",
		"Enter the map pool name or index: "
	)
	map_pool_path = os.path.join("compose", "maps", str(map_pool))
	
	# List and select map order
	maps = os.listdir(map_pool_path)
	ordered_map_pool = selector(
		maps, 
		f"Available maps in {map_pool}:",
		"Enter the map names or indexes separated by spaces (order matters): ",
		unique_choice=False
	)

	# Build config file tree from scratch
	playlist_el = etree.Element("playlist")
	
	handlers = {
		"gameinfo": handle_gameinfo,
		"script_settings": handle_script_settings
	}

	for key, value in settings[config_name].items():
		if key in handlers:
			handlers[key](playlist_el, value)
		else:
			etree.SubElement(playlist_el, key).text = to_tm_val(value)

	# Add maps
	for map_name in ordered_map_pool:
		map_subel = etree.SubElement(playlist_el, "map")
		etree.SubElement(map_subel, "file").text = f"{map_pool}/{map_name}"

	# Write config to a temporary file
	with open("cfg_to_copy.xml", "w+", encoding="utf-8") as f:
		f.write(xml.dom.minidom.parseString(
			etree.tostring(playlist_el, encoding='utf-8')
		).toprettyxml(indent="  "))

	# Apply configuration to selected cups
	for cup in selected_cups:
		if os.path.exists(f"compose/{cup}/maps/MatchSettings/cfg_tracklist.xml"):
			os.popen(f"cp compose/{cup}/maps/MatchSettings/cfg_tracklist.xml compose/{cup}/maps/MatchSettings/cfg_tracklist.xml.old")
		os.popen(f"cp cfg_to_copy.xml compose/{cup}/maps/MatchSettings/cfg_tracklist.xml")


if __name__ == "__main__":
	main()