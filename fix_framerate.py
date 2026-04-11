import json

file_path = 'WebUI/external/presets/LTX-Video.json'
with open(file_path, 'r') as f:
    data = json.load(f)

if 'settings' in data:
    for setting in data['settings']:
        if setting.get('label') == 'Frame Rate':
            print("Found in top level:", setting)
            setting.pop('min', None)
            setting.pop('max', None)
            setting.pop('step', None)

if 'pipelines' in data:
    for preset in data['pipelines']:
        if 'settings' in preset.get('overrides', {}):
            for setting in preset['overrides']['settings']:
                if setting.get('label') == 'Frame Rate':
                    print("Found in pipeline overrides:", setting)
                    setting.pop('min', None)
                    setting.pop('max', None)
                    setting.pop('step', None)

        if 'settings' in preset:
            for setting in preset['settings']:
                if setting.get('label') == 'Frame Rate':
                    print("Found in pipeline:", setting)
                    setting.pop('min', None)
                    setting.pop('max', None)
                    setting.pop('step', None)

with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)
