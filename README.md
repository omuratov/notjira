# NOTJIRA a programmer friendly task planning


## Usage

```python
from notjira.task import Task, TimeEstimate, Epic
from notjira.utils import dependency_list, gantt_ascii
from notjira.chart import gantt_matplotlib


# creating a task
sample_task = Task(name='a sample task', estimate='1h', due_date='2024-01-01' )
print('Sample_task\n', sample_task)

# print where tasks are stored?
from notjira.context import PlanContext
print("Sample task using plan\n", PlanContext().default_plan.get_item(sample_task.id))

# creating an epic
sample_epic = Epic('Sample epic')
print('Sample epic\n', sample_epic)
# or
another_task = Task('another task', e='2h')
another_epic = sample_task + another_task
print('Another epic\n', another_epic)

# Making dependencies
test_sample_task = Task('test sample task', e='2h', d=sample_task)
print('Task depends on task ids\n', test_sample_task.depends)

# Build dependency chain
task_a = Task('a')
task_b = Task('b', d=task_a)
task_c = Task('c', d=task_b)
task_d = Task('d', d=task_c)
task_e = Task('e', d=task_c)

assert task_a.id in dependency_list(task_d)
assert task_e.id not in dependency_list(task_d)

# Gantt chart (ASCII)
print(gantt_ascii())

# Gantt chart (matplotlib)
# Requires: pip install matplotlib
gantt_matplotlib(filename='plan.png')
# Epic summary only
gantt_matplotlib(filename='plan_epics.png', epic_only=True)
print('Saved to plan.png')
```

## Concepts
TODO

## Packaging

Build and publish (requires build tool):

```bash
python -m pip install --upgrade pip build twine
python -m build
twine check dist/*
twine upload dist/*  # requires credentials
```

Install locally for development editable mode:

```bash
pip install -e .
```

Minimal dependencies: core library works without matplotlib (only ASCII Gantt). Install optional extras:

```bash
pip install notjira[all]
```
