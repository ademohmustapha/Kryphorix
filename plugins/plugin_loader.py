import importlib
import os

def load_plugins():
    plugins = []
    plugins_dir = "plugins"
    if not os.path.exists(plugins_dir):
        return plugins  # No plugins folder

    for file in os.listdir(plugins_dir):
        if file.endswith(".py") and not file.startswith("_") and file != "plugin_loader.py":
            name = file[:-3]
            try:
                module = importlib.import_module(f"plugins.{name}")
                if hasattr(module, "run") and callable(module.run):
                    plugins.append(module.run)
            except Exception as e:
                print(f"[!] Failed to load plugin {name}: {e}")
    return plugins

