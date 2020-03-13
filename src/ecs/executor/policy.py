from typing import (
    Mapping,
    Tuple,
    Callable,
    Any,
)


class ResumePolicy:
    ...


class AsyncWait(ResumePolicy):

    # should be Callable[..., Any] but mypy thinks its a method
    # and doesn't allow any assignments
    func: Any
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class Defer(ResumePolicy):
    ...


defer = Defer
