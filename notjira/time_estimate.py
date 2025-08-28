class TimeEstimate:
    def __init__(self, value_hours=0):
        self._value = value_hours
        
    def __repr__(self):
        if self.weeks > 1:
            return f"{self.weeks:0.1f}w"
        elif self.days > 1:
            return f"{self.days:0.1f}d"
        else:
            return f"{self.hours:0.1f}h"

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return TimeEstimate(self._value * other)
        else:
            raise
        
    def __add__(self, other):
        if isinstance(other, TimeEstimate):
            return TimeEstimate(value_hours=(self.hours + other.hours))
        elif other is None:
            return self
        elif isinstance(other, list):
            for item in other:
                self += item 
            return self 
        else:
            try:
                return other.estimate + self
            except:
                print("Cannot sum up")
            raise
        
    @property
    def weeks(self):
        return self._value / (8*5)
        
    @property
    def days(self):
        return self._value / 8
    
    @property
    def hours(self):
        return self._value
    
    @staticmethod
    def auto(input_value):
        if isinstance(input_value, TimeEstimate):
            return input_value
        elif isinstance(input_value, str):
            return TimeEstimate.from_string(input_value)
        elif input_value is None:
            return input_value
        else:
            raise
    
    @staticmethod
    def from_string(string_value):
        if string_value[-1] == 'd':
            hours = float(string_value.split('d')[0]) * 8
        elif string_value[-1] == 'w':
            hours = float(string_value.split('w')[0]) * 8 * 5
        elif string_value[-1] == 'h':
            hours = float(string_value.split('h')[0])
        else:
            raise
        return TimeEstimate(hours)
