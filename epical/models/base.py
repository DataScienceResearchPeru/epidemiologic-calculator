from abc import ABC


class Covid19Interface(ABC):
    # Since this class is a subclass of ABC its methods are abstract
    # @abstractmethod
    def model(self, initial_conditions, duration, epidemiological_parameters):
        # pylint: disable=misplaced-bare-raise
        raise NotImplementedError("Needs to be implemented by subclasses")
