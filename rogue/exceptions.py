class QuitGameException(Exception):
    """
    raise QuitGameException to exit the game
    """

    ...


class IgnoreTimeStepException(Exception):
    """
    raise IgnoreTimeStepException to ignore all of the updates for the current time step
    """

    ...
