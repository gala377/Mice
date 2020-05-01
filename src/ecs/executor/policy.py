from typing import (
    Mapping,
    Tuple,
    Callable,
    Any,
    Sequence,
    Optional,
)


class ResumePolicy:
    
    def tag(self):
        raise NotImplementedError(f"{self.__class__.__name__} doesn't implement ResumePolicy's tag method")

class AsyncWait(ResumePolicy):

    func: Callable[..., Any]
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    TAG = 2

    def tag(self):
        return self.TAG


class Defer(ResumePolicy):
    
    TAG = 1

    def tag(self):
        return self.TAG


class Terminate(ResumePolicy):

    TAG = 3

    def tag(self):
        return self.TAG


class Pause(ResumePolicy):

    TAG = 4

    def tag(self):
        return self.TAG


class Restart(ResumePolicy):

    TAG = 5
    def tag(self):
        return self.TAG


class Unpause(ResumePolicy):

    TAG = 6
    system: str

    def __init__(self, system: str, with_args: Optional[Sequence[Any]] = None):
        self.with_args = with_args
        self.system = system

    def tag(self):
        return self.TAG


class Start(ResumePolicy):

    TAG = 7
  
    system_instance: Any
    system_name: str

    def __init__(self, system_instance: Any, name: str = None):
        self.system_instance = system_instance
        if name is None:
            name = system_instance.__class__.__name__
        self.system_name = name 

    def tag(self):
        return self.TAG


defer = Defer()
terminate = Terminate()
pause = Pause()
restart = Restart()
