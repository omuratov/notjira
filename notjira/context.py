
class Plan:
    def __init__(self, make_default=True):
        self._id_counter = 0
        self._item_pool = dict()
        if make_default:
            self.make_default()
        
    def register_item(self, task):
        new_id = self._id_counter
        self._id_counter += 1
        task.set_id(new_id)
        self._item_pool[new_id] = task
        
    def deregister_item(self, task_id):
        del self._item_pool[task_id]
    
    def make_default(self):
        PlanContext().default_plan = self
    
    def get_item(self, item_id):
        return self._item_pool[item_id]



class PlanContext(object):
    _context = None
    
    def __new__(cls):
        if cls._context is None:
            print('creating new PlanContext')
            cls._context = super(PlanContext, cls).__new__(cls)
            cls._context.default_plan = None
        return cls._context
        
    @property
    def default_plan(self) -> Plan:
        return self._default_plan
    
    @default_plan.setter
    def default_plan(self, new_plan):
        self._default_plan = new_plan



default_plan = Plan()
