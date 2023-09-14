from task_lib.time_estimate import TimeEstimate
from task_lib.context import PlanContext

from enum import Enum

class BaseStatus(Enum):
   OPEN="open",
   IN_PROGRESS="in progress"
   DONE="done"
   CLOSED="closed"


def depends_auto(items):
  if items is None:
    return set()
  if isinstance(items, Base):
      return {items.id}
  return {x.id for x in items}



class Base:
    def __init__(self, name=None, depends=None, estimate=None, due_date=None, **kw):
        self._name = name
        self._depends = depends_auto(depends)
        self._estimate = TimeEstimate.auto(estimate)
        self._due_date = due_date
        self._id = None
        self._status = BaseStatus.OPEN
        for key, value in kw.items():
            if key == 'n' and name is None:
                self._name = value
            elif key == 'e' and estimate is None:
                self._estimate = TimeEstimate.auto(value)
            elif key == 'dd' and due_date is None:
                self._due_date = value
            elif key == 'd' and depends is None:
                self._depends = depends_auto(value)
        PlanContext().default_plan.register_item(self)

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    
    def set_id(self, new_id):
        self._id = new_id
        
    @property
    def name(self):
        return self._name
        
    @property
    def depends(self):
        return self._depends

    def add_dependency(self, item):
        new_deps = depends_auto([item])
        for item in new_deps:
            self._depends.add(item)

    def remove_dependency(self, other):
        if other.id in self._depends:
            self._depends.remove(other.id)
            return
        else:
            print(f'Warning: no such dependency {other}')
    
    @property
    def estimate(self):
        return self._estimate

        
