#!/bin/python3

from lxml import etree
from argparse import ArgumentParser
import json
import os

parser = ArgumentParser()
parser.add_argument("maps", help="Map folder name in compose/maps")
parser.add_argument("config", help="Name of the config")
args = parser.parse_args()

settings = json.load(open("config.json", "r"))
rel_path = os.path.join("compose", "maps", args.maps)
maps = {i: m for i, m in enumerate(os.listdir(rel_path))}

print(f"Available maps in {args.maps}:")
for i in range(len(maps)):
    print(f"  {i} - {maps[i].split('.')[0]}")

with open("cfg_to_copy.xml", "w+", encoding="utf-8") as f:
    playlist = etree.Element("playlist")
    gameinfos = etree.SubElement(playlist, "gameinfos")
    etree.SubElement(gameinfos, "game_mode").text = str(settings[args.config]["gameinfo"]["game_mode"])
    etree.SubElement(gameinfos, "script_name").text = str(settings[args.config]["gameinfo"]["script_name"])

    filter = etree.SubElement(playlist, "filter")
    etree.SubElement(filter, "is_lan").text = "1" if settings[args.config]["gameinfo"]["filter"]["is_lan"] else "0"
    etree.SubElement(filter, "random_map_order").text = "1" if settings[args.config]["gameinfo"]["filter"]["random_map_order"] else "0"

    script_settings = etree.SubElement(playlist, "script_settings")
    for key, value in settings[args.config]["script_settings"].items():
        setting = etree.SubElement(script_settings, "setting")
        setting.set("name", key)
        if isinstance(value, int):
            setting.set("type", "integer")
        elif isinstance(value, bool):
            setting.set("type", "boolean")
        else:
            setting.set("type", "string")
        setting.set("value", ",".join(str(i) for i in value) if isinstance(value, list) else str(value))

    etree.SubElement(playlist, "startindex").text = str(settings[args.config]["startindex"])

    for i in input("Enter the ordered map indexes separated by a space: ").split():
        map = etree.SubElement(playlist, "map")
        etree.SubElement(map, "file").text = f"{args.maps}/{maps[int(i)]}"

    f.write("<?xml version='1.0' encoding='utf-8'?>\n")
    f.write(etree.tostring(playlist, pretty_print=True).decode('utf-8'))

for cup in os.listdir("compose"):
    if "cup" in cup:
        os.popen(f"cp compose/{cup}/maps/MatchSettings/cfg_tracklist.xml compose/{cup}/maps/MatchSettings/cfg_tracklist.xml.old")
        os.popen(f"cp cfg_to_copy.xml compose/{cup}/maps/MatchSettings/cfg_tracklist.xml")