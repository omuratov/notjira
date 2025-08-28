from notjira.base import Base
from notjira.time_estimate import TimeEstimate
from notjira.context import PlanContext


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
    def __init__(self, name=None, tasks=None, chain=True, **kw):
        """Epic groups tasks and aggregates their estimates.

        Args:
            name: Epic name
            tasks: Optional iterable of Task objects
            chain: If True, each task after the first depends on the previous
                   task (A -> B -> C). Existing dependencies are preserved.
            **kw: Shorthand keys (n,e,...) passed to Base
        """
        super(Epic, self).__init__(name=name, **kw)
        self._estimate = TimeEstimate(0)
        self._tasks = [x for x in tasks] if tasks is not None else []
        if chain and len(self._tasks) > 1:
            prev = None
            for t in self._tasks:
                if prev is not None:
                    t.add_dependency(prev)
                prev = t
        # If this epic depends on other epics, link first task to those epics' last task
        if self._tasks:
            first = self._tasks[0]
            for dep_id in list(self.depends):
                try:
                    dep_item = PlanContext().default_plan.get_item(dep_id)
                except KeyError:
                    continue
                if isinstance(dep_item, Epic) and dep_item.tasks:
                    # assume provided order or existing chain; last task is completion
                    first.add_dependency(dep_item.tasks[-1])
        self.recalculate_estimate()

    def add_dependency(self, item):
        """Add a dependency to the epic and propagate to its first task.

        If the dependency is another Epic, the first task of this epic will
        depend on the last task of that epic. If it's a Task, the first task
        depends directly on it.
        """
        super().add_dependency(item)
        if not self._tasks:
            return
        first = self._tasks[0]
        try:
            from notjira.task import Epic as EpicClass  # local import to avoid circular
        except Exception:
            EpicClass = Epic  # fallback
        if isinstance(item, EpicClass):
            if item.tasks:
                first.add_dependency(item.tasks[-1])
        elif isinstance(item, Task):
            first.add_dependency(item)
        return self


    def recalculate_estimate(self):
        self._estimate = TimeEstimate(0)
        for task in self._tasks:
            self._estimate += task.estimate
            
    def __add__(self, other):
        if isinstance(other, Task):
            self._tasks.append(other)
            self.recalculate_estimate()
            return self
        elif isinstance(other, Epic):
            return self.estimate + other.estimate
        elif isinstance(other, TimeEstimate):
            return self.estimate + other
        elif isinstance(other, list):
            for item in other:
                self += item
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
