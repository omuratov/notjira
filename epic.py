from task_lib.task import Task, TimeEstimate
from task_lib.context import PlanContext

class NotEpic:
    def __init__(self, name=None, tasks=None, estimate=None):
        self._name = name
        self._id = None
        if tasks is not None:
            self._tasks = [x for x in tasks]
        else:
            self._tasks = list()
        self._estimate = estimate
        PlanContext().default_plan.register_item(self)
        

    @property
    def id(self):
        return self._id

    def set_id(self, new_id):
        self._id = new_id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name
    
    @property
    def estimate(self):
        return self._estimate
    
    def recalculate_estimate(self):
        self._estimate = TimeEstimate(0)
        for task in self._tasks:
            self._estimate += task.estimate
            
    def __add__(self, other):
        if isinstance(other, Task):
            self._tasks.append(other)
            self.recalculate_estimate()
            return self
        else:
            raise
                
    @property
    def tasks(self):
        return self._tasks
    
    @tasks.setter
    def tasks(self, tasks):
        self.tasks = [x for x in tasks]
        
    def __repr__(self):
        repr_string = f"<Epic {self.id} {self.name} tasks:\n"
        for task in self._tasks:
            repr_string += f"{task.id}:  {task.name}  {task.estimate}\n"
        repr_string += f"Total estimate {self.estimate}"
        return repr_string
