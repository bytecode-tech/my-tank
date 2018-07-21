from gpiozero import DigitalOutputDevice, OutputDevice

class Relay(OutputDevice):
    """
    Represents a generic relay with typical on/off behaviour.

    This class extends :class:`OutputDevice` and sets the default active_high to 
    False
    """
    def __init__(
            self, pin=None, active_high=False, initial_value=False,
            pin_factory=None):
        super(DigitalOutputDevice, self).__init__(
            pin, active_high, initial_value, pin_factory=pin_factory
        )
