from notjira.time_estimate import TimeEstimate
from notjira.context import PlanContext
from datetime import date, timedelta

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
    def __init__(self, name=None, depends=None, estimate=None, due_date=None, start_date=None, **kw):
        self._name = name
        self._depends = depends_auto(depends)
        self._estimate = TimeEstimate.auto(estimate)
        self._due_date = due_date
        self._id = None
        self._status = BaseStatus.OPEN
        # scheduling attributes (optional)
        self._start_date = start_date
        self._end_date = None
        for key, value in kw.items():
            if key == 'n' and name is None:
                self._name = value
            elif key == 'e' and estimate is None:
                self._estimate = TimeEstimate.auto(value)
            elif key == 'dd' and due_date is None:
                self._due_date = value
            elif key == 'd' and depends is None:
                self._depends = depends_auto(value)
            elif key == 'sd' and start_date is None:
                self._start_date = value
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
        # Lazy import to avoid circular dependency
        try:
            from notjira.utils import dependency_list
        except Exception:
            dependency_list = None
        for dep_id in new_deps:
            # Skip if already present
            if dep_id in self._depends:
                continue
            # Only check cycles if we can access dependency_list and we already have an id
            if dependency_list is not None and self._id is not None:
                try:
                    # If adding dep_id would make a cycle, then self is reachable from dep_id
                    if self._id == dep_id:
                        raise ValueError("Cannot depend on itself")
                    if self._id in dependency_list(dep_id):
                        raise ValueError(f"Adding dependency creates cycle: {self._id} <- ... <- {dep_id}")
                except KeyError:
                    # If dep item not yet registered, ignore cycle check
                    pass
            self._depends.add(dep_id)

    def remove_dependency(self, other):
        if other.id in self._depends:
            self._depends.remove(other.id)
            return
        else:
            print(f'Warning: no such dependency {other}')
    
    @property
    def estimate(self):
        return self._estimate

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, new_start):
        self._start_date = new_start
        self._end_date = None  # invalidate

    @property
    def end_date(self):
        return self._end_date

    def compute_end_date(self):
        if self._start_date is None:
            return None
        # Assume 1 day if estimate missing
        if self._estimate is None:
            self._end_date = self._start_date
            return self._end_date
        # number of work days (ceil) based on 8h days
        hours = self._estimate.hours
        if hours == 0:
            self._end_date = self._start_date
            return self._end_date
        work_days = int((hours + 7) // 8)  # ceil
        current = self._start_date
        days_added = 0
        while days_added < work_days - 1:  # end date inclusive; 1 day task ends same day
            current += timedelta(days=1)
            if current.weekday() < 5:
                days_added += 1
        self._end_date = current
        return self._end_date

        
