from notjira.task import Task, Epic
from notjira.chart import gantt_matplotlib

epic_prepare = Epic('Preparation work', tasks=[
    Task('Ask everyone what to do', e='2w'),
    Task('Create spec sheet', e='1w'),
    Task('Talk to the expert to get time estimates', e='1w'),
    Task('Populate plan', e='2w')])



epic_execute = Epic('Execute stage', tasks=[
    Task('Kick off project with the team', e='1w'),
    Task('Assign responsible for deliverables', e='2w'),
    Task('Verify milestone deliverables', e='2w'),
    Task('Update reports', e='2w'),
    Task('Prepare demo', e='1w')])
epic_execute.add_dependency(epic_prepare)
total_estimate = epic_prepare + epic_execute
print(f'Total estimate: {total_estimate}')
gantt_matplotlib(filename="example_gantt.png", epic_only=True)