import os
import importlib

config_dir = os.path.dirname(__file__)

# Iterasi file di direktori config_dir
for config_fname in os.listdir(config_dir):
    if config_fname.lower().endswith('.py') and not config_fname.startswith('__'):
        module_name = config_fname[:-3]
        module = importlib.import_module(f'backend.config.{module_name}')
        for param in [x for x in dir(module) if not x.startswith('__')]:
            obj = module.__getattribute__(param)
            if param in globals():
                previous_obj = globals()[param]
                if type(previous_obj) == dict and type(obj) == dict:
                    updated = True
                    if 'update_previous' in obj:
                        updated = obj['update_previous']
                    if updated:
                        previous_obj.update(obj)
            else:
                globals()[param] = obj
