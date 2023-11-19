import importlib, os
import inspect

modules_loaded = []

module_dir = "src/services"
module_files = [
    f[:-3]
    for f in os.listdir(module_dir)
    if f.endswith(".py") and not f.startswith("__")
]
for module_name in module_files:
    module = importlib.import_module(f"{module_dir.replace('/', '.')}.{module_name}")

    # Obtém todas as classes do módulo
    classes = inspect.getmembers(module, inspect.isclass)

    # Instancia todas as classes encontradas
    for class_name, class_obj in classes:
        if class_name.endswith("Service"):
            instance = class_obj()
            globals()[f"{instance.entity}_service"] = instance
            modules_loaded.append(f"{instance.entity}_service")

