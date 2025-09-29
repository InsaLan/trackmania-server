#!/bin/python3

import xml.etree.ElementTree as etree
import json
import os
import xml.dom.minidom

def selector(pool: dict[int, str], q_str: str, a_str: str, unique_choice: bool = True) -> str | list[str]:
	print(q_str)
	for i, key in pool.items():
		print(f"	{i} - {key}")
	choices = input(a_str).strip().split()
	if unique_choice and len(choices) > 1:
		print("Only one choice is allowed. Exiting.")
		exit(1)
	res = []
	for choice in choices:
		if choice.isdigit() and int(choice) in pool.keys():
			res.append(pool[int(choice)])
		elif choice in pool.values():
			res.append(choice)
		else:
			print(f"Choice '{choice}' not found. Exiting.")
			exit(1)
	if unique_choice:
		return res[0]
	return res

def main() -> None:

	settings = json.load(open("config.json", "r"))
	configs: dict[int, str] = {i: c for i, c in enumerate(settings.keys())}
	config_name = str(selector(configs, "Available configurations in config.json:", "Enter the configuration name or index: "))

	map_pools: dict[int, str] = {i: m for i, m in enumerate(os.listdir(os.path.join("compose","maps")))}
	map_pool = selector(map_pools, "Available map pools in compose/maps:", "Enter the map pool name or index: ")
	map_pool_path = os.path.join("compose", "maps", str(map_pool))
	
	maps = {i: m for i, m in enumerate(os.listdir(map_pool_path))}
	ordered_map_pool = selector(maps, f"Available maps in {map_pool}:", "Enter the map names or indexes separated by spaces (order matters): ", unique_choice=False)

	with open("cfg_to_copy.xml", "w+", encoding="utf-8") as f:
		playlist_el = etree.Element("playlist")
		gameinfos_subel = etree.SubElement(playlist_el, "gameinfos")
		etree.SubElement(gameinfos_subel, "game_mode").text = str(settings[config_name]["gameinfo"]["game_mode"])
		etree.SubElement(gameinfos_subel, "script_name").text = str(settings[config_name]["gameinfo"]["script_name"])

		filter_subel = etree.SubElement(playlist_el, "filter")
		etree.SubElement(filter_subel, "is_lan").text = "1" if settings[config_name]["gameinfo"]["filter"]["is_lan"] else "0"
		etree.SubElement(filter_subel, "random_map_order").text = "1" if settings[config_name]["gameinfo"]["filter"]["random_map_order"] else "0"

		script_settings_subel = etree.SubElement(playlist_el, "script_settings")
		for key, value in settings[config_name]["script_settings"].items():
			setting_subel = etree.SubElement(script_settings_subel, "setting")
			setting_subel.set("name", key)
			if isinstance(value, int):
				setting_subel.set("type", "integer")
			elif isinstance(value, bool):
				setting_subel.set("type", "boolean")
			else:
				setting_subel.set("type", "string")
			setting_subel.set("value", ",".join(str(i) for i in value) if isinstance(value, list) else str(value))

		etree.SubElement(playlist_el, "startindex").text = str(settings[config_name]["startindex"])

		for map in ordered_map_pool:
			map_subel = etree.SubElement(playlist_el, "map")
			etree.SubElement(map_subel, "file").text = f"{map_pool}/{map}"

		xml_str = etree.tostring(playlist_el, encoding='utf-8')
		pretty_xml = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="  ")
		f.write(pretty_xml)

	for cup in os.listdir("compose"):
		if "cup" in cup:
			os.popen(f"cp compose/{cup}/maps/MatchSettings/cfg_tracklist.xml compose/{cup}/maps/MatchSettings/cfg_tracklist.xml.old")
			os.popen(f"cp cfg_to_copy.xml compose/{cup}/maps/MatchSettings/cfg_tracklist.xml")

if __name__ == "__main__":
	main()