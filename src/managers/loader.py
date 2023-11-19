from src.managers.abstract_manager import AbstractManager
from src.repositorys import provider_repo, credential_repo
import importlib


consumer_repo_module = importlib.import_module("src.repository.consumer")
consumer_repo = consumer_repo_module.ConsumerRepository()


def load_managers_by_consumers(consumer_id: str):
    consumer = consumer_repo.get_aggregate_data(consumer_id)
    if not consumer:
        raise Exception("consumer not found")
    managers = []
    for cred in consumer.get("credentials"):
        managers.append(load_manager(cred))
    return managers


def load_manager(credential: dict, consumer_id: str = None) -> AbstractManager:
    if type(credential) == str:
        credential = credential_repo.get(credential)
    client_loaded = credential.get("provider")
    if client_loaded and type(client_loaded) is str:
        client_loaded = provider_repo.get(client_loaded)
    name = client_loaded.get("name").lower()
    class_name = f"{name.title()}Manager"
    manager = getattr(
        importlib.import_module(f"src.clients.{name}.manager"), class_name
    )
    return {
        "name": client_loaded.get("name"),
        "instance": manager(credential.get("keys"), credential.get("id"), consumer_id),
        "type": client_loaded.get("type").upper(),
        "credential_id": credential.get("id"),
        "credential_data": credential,
    }


def found_manager(managers, key: str, value: str):
    found_manager = None
    for manager in managers:
        if manager.get(key) == value:
            found_manager = manager
            break
    return found_manager
