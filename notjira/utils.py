from notjira.context import PlanContext 
from notjira.base import Base
from datetime import date, timedelta


def dependency_list(task_or_task_id):
    if isinstance(task_or_task_id, Base):
       task_id = task_or_task_id.id
    else:
       task_id = task_or_task_id
    visit_queue = list()
    dependencies = set()
    visit_queue.append(task_id)
    while len(visit_queue):
       c_item = visit_queue[0]
       del visit_queue[0]
       other_item = PlanContext().default_plan.get_item(c_item)
       for x in other_item.depends:
           if x in dependencies:
               continue
           dependencies.add(x)
           visit_queue.append(x)
    return dependencies


def _topological_sort(items):
   # Kahn's algorithm
   indeg = {x.id:0 for x in items}
   graph = {x.id:set() for x in items}
   for x in items:
      for d in x.depends:
         graph[d].add(x.id)
         indeg[x.id] += 1
   queue = [i for i, v in indeg.items() if v == 0]
   ordered = []
   while queue:
      n = queue.pop(0)
      ordered.append(n)
      for m in graph[n]:
         indeg[m]-=1
         if indeg[m]==0:
            queue.append(m)
   if len(ordered)!=len(items):
      raise RuntimeError("Cycle detected in dependencies")
   id_to_item = {x.id:x for x in items}
   return [id_to_item[i] for i in ordered]


def schedule(plan=None, start_date=None):
   """Assign start/end dates to tasks in a plan using ASAP scheduling.

   Args:
      plan: Plan instance or None for default
      start_date: date to begin (defaults to today)
   Returns: list of (task, start_date, end_date)
   """
   if plan is None:
      plan = PlanContext().default_plan
   if start_date is None:
      start_date = date.today()
   tasks = [t for t in plan.items() if isinstance(t, Base)]
   ordered = _topological_sort(tasks)
   id_to_task = {t.id:t for t in tasks}
   task_dates = {}
   for task in ordered:
      # earliest dependency end date (if any)
      if task.depends:
         dep_end = None
         for d in task.depends:
            candidate_end = task_dates[d][1]
            dep_end = candidate_end if dep_end is None else max(dep_end, candidate_end)
         # start day is the next calendar day after dep_end
         dep_start = dep_end + timedelta(days=1)
      else:
         dep_start = start_date
      # bump to weekday if weekend
      while dep_start.weekday() >= 5:
         dep_start += timedelta(days=1)
      task.start_date = dep_start
      end_date = task.compute_end_date()
      # If computed end falls on weekend due to zero estimate handling, okay; duration calc in Base already skips weekends for counting
      task_dates[task.id] = (task.start_date, end_date)
   return [(id_to_task[i], *task_dates[i]) for i in task_dates]


def gantt_ascii(plan=None, start_date=None):
   """Return a simple ASCII Gantt chart string."""
   sched = schedule(plan, start_date)
   if not sched:
      return "<empty plan>"
   min_start = min(s for _,s,_ in sched)
   max_end = max(e for _,_,e in sched)
   total_days = (max_end - min_start).days + 1
   lines = []
   header = "Date    |" + ''.join((min_start + timedelta(days=i)).strftime('%d') for i in range(total_days))
   lines.append(header)
   lines.append('-'*len(header))
   for task, s, e in sched:
      start_offset = (s - min_start).days
      end_offset = (e - min_start).days
      bar = ''.join('#' if start_offset <= i <= end_offset else ' ' for i in range(total_days))
      lines.append(f"{task.name[:7]:7}|{bar}")
   return '\n'.join(lines)

        
       
    
