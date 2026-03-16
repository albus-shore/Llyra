from .untils.classes import CallStrategyData, ChatStrategyData
from dataclasses import dataclass

## =========================== `StrategyData` Dataclass =========================== ##
@dataclass(frozen=True)
class StrategyData:
    '''This class is a dataclass contains information for inference strategy control.
    Args:
        call: A `CallStrategyData` instance indicates 
            the strategy used for call inference.
        chat: A `ChatStrategyData` instance indicates 
            the strategy used for chat inference.
    '''
    call: CallStrategyData | False
    chat: ChatStrategyData | False