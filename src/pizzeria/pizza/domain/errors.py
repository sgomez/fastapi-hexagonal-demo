from pizzeria.system.domain.errors import LogicDomainError


class DuplicatedNameError(LogicDomainError):
    def __init__(self, name: str):
        super().__init__(f"Duplicated name {name}", "name", "pizza_duplicated_name")
