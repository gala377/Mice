from typing import (
    Mapping,
    Tuple,
    Callable,
    Any,
)


class ResumePolicy:
    ...


class AsyncWait(ResumePolicy):

    func: Callable[..., Any]
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs


class Defer(ResumePolicy):
    ...


defer = Defer()
