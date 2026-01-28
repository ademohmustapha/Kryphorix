import importlib
import os

def load_plugins():
    plugins = []
    for file in os.listdir("plugins"):
        if file.endswith(".py") and file != "plugin_loader.py":
            name = file[:-3]
            module = importlib.import_module(f"plugins.{name}")
            if hasattr(module, "run"):
                plugins.append(module.run)
    return plugins

