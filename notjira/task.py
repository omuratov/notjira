from task_lib.base import Base
from task_lib.time_estimate import TimeEstimate


class Task(Base):
    def __init__(self, name=None, **kw):
       super(Task, self).__init__(name=name, **kw)
       
    def __repr__(self):
        return f"<Task {self._id} {self._name} {self._estimate}>"
    
    def __add__(self, other):
        if isinstance(other, Task):
            epic = Epic(tasks=[self, other])
            epic.recalculate_estimate()
            return epic
        else:
            raise


class Epic(Base):
    def __init__(self, name=None, tasks=None, **kw):
        super(Epic, self).__init__(name=name, **kw)
        if tasks is not None:
            self._tasks = [x for x in tasks]
        else:
            self._tasks = list()
        for key, value in kw:
           if key == 'tasks' and tasks is None:
               self._tasks = [x for x in value]

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
