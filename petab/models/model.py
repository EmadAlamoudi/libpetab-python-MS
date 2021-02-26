"""PEtab model abstraction"""

from typing import Iterable, Tuple
import abc


class Model:
    """Base class for wrappers for any PEtab-supported model type"""

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_parameter_ids(self) -> Iterable[str]:
        pass

    @abc.abstractmethod
    def get_parameter_ids_with_values(self) -> Iterable[Tuple[str, float]]:
        pass

    @abc.abstractmethod
    def has_species_with_id(self, entity_id: str) -> bool:
        pass

    @abc.abstractmethod
    def has_compartment_with_id(self, entity_id: str) -> bool:
        pass

    @abc.abstractmethod
    def has_entity_with_id(self, entity_id) -> bool:
        pass

    @abc.abstractmethod
    def get_valid_parameters_for_parameter_table(self) -> Iterable[str]:
        pass


