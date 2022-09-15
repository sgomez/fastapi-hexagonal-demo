from typing import Type

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher
from requests import Response

from pizzeria.system.strawberry.errors import Error


class ErrorInResponse(BaseMatcher[Type[Error]]):
    """Custom matcher to detect errors in response."""

    def __init__(self, response: Response) -> None:
        self.response = response

    def _matches(self, item: Type[Error]) -> bool:
        try:
            content = self.response.json()
            errors = content["data"]["addPizza"]["errors"]
        except KeyError:
            return False

        for error in errors:
            if error.get("__typename") == item.__name__:
                return True

        return False

    def describe_to(self, description: Description) -> None:
        """Generates a description of the matcher."""
        description.append_text("error not in response: ").append_text(self.response.text)


def error_in_response(response: Response) -> Matcher[Type[Error]]:
    """Matcher ErrorInResponse factory method."""
    return ErrorInResponse(response)
