import json
import os


def load_settings_dict(file_path):
	f = open(file_path)
	json_obj = json.loads(f.read())
	f.close()
	return json_obj