import importlib, os
import inspect

modules_loaded = []

module_dir = "src/repositorys"
module_files = [
    f[:-3]
    for f in os.listdir(module_dir)
    if f.endswith(".py") and not f.startswith("__")
]
for module_name in module_files:
    module = importlib.import_module(f"{module_dir.replace('/', '.')}.{module_name}")
    classes = inspect.getmembers(module, inspect.isclass)

    for class_name, class_obj in classes:
        if class_name.endswith("Repository"):
            instance = class_obj()
            if instance.entity.endswith("s"):
                globals()[f"{instance.entity[:-1]}_repo"] = instance
                modules_loaded.append(f"{instance.entity[:-1]}_repo")
                continue
            globals()[f"{instance.entity}_repo"] = instance
            modules_loaded.append(f"{instance.entity}_repo")

print(modules_loaded)