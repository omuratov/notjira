from task_lib.context import PlanContext 
from task_lib.base import Base


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
        
       
    
