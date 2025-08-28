"""Chart utilities for notjira.

Provides matplotlib based Gantt chart rendering.
"""

from datetime import date
from pathlib import Path
from typing import Optional, List, Tuple

from .utils import schedule
from .task import Epic, Task
from .context import PlanContext

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

ScheduleEntry = Tuple[Task, date, date]


def _aggregate_epics(sched: List[ScheduleEntry], plan) -> List[ScheduleEntry]:
    """Aggregate task schedule into epic windows."""
    items = plan.items()
    epics = [x for x in items if isinstance(x, Epic)]
    task_to_epic = {t.id: epic for epic in epics for t in epic.tasks}
    epic_windows = {}
    for task, s, e in sched:
        parent = task_to_epic.get(task.id)
        if parent is None:
            continue
        win = epic_windows.get(parent.id)
        if win is None:
            epic_windows[parent.id] = [parent, s, e]
        else:
            win[1] = min(win[1], s)
            win[2] = max(win[2], e)
    return [tuple(v) for v in epic_windows.values()]


def _prepare_schedule(plan, start_date, epic_only: bool) -> List[ScheduleEntry]:
    if plan is None:
        plan = PlanContext().default_plan
    sched = schedule(plan, start_date)
    if not sched:
        raise ValueError("Plan is empty; nothing to plot.")
    if epic_only:
        sched = _aggregate_epics(sched, plan)
        if not sched:
            raise ValueError("No epic data to plot.")
    sched.sort(key=lambda x: (x[1], x[0].name))
    return sched


def _plot_schedule(sched: List[ScheduleEntry], figsize, title: str):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError as e:
        raise ImportError("matplotlib is required for plotting. Install with 'pip install matplotlib'.") from e
    min_start = min(s for _, s, _ in sched)
    max_end = max(e for _, _, e in sched)
    task_count = len(sched)
    height = max(2, task_count * 0.4)
    fig, ax = plt.subplots(figsize=(figsize[0], height))
    for idx, (task, s, e) in enumerate(sched):
        start_num = mdates.date2num(s)
        end_num = mdates.date2num(e) + 1
        ax.barh(idx, end_num - start_num, left=start_num, height=0.3, align='center')
        ax.text(start_num, idx, f" {task.estimate}", va='center', ha='left', fontsize=8)
    ax.set_yticks(range(task_count))
    ax.set_yticklabels([t.name for t, _, _ in sched])
    ax.invert_yaxis()
    ax.xaxis_date()
    import matplotlib.dates as mdates  # reuse
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate(rotation=30, ha='right')
    ax.set_xlabel('Date')
    ax.set_title(title)
    today = date.today()
    if min_start <= today <= max_end:
        ax.axvline(mdates.date2num(today), color='red', linestyle='--', linewidth=1)
    fig.tight_layout()
    return fig, ax


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def gantt_matplotlib(plan=None, start_date: Optional[date] = None, filename: str = "gantt.png", figsize=(10, 0.5), epic_only: bool = False):
    """Render a Gantt chart of the plan to a PNG file using matplotlib."""
    sched = _prepare_schedule(plan, start_date, epic_only)
    title = 'Plan Gantt' + (' [Epics]' if epic_only else '')
    fig, ax = _plot_schedule(sched, figsize, title)
    from matplotlib import pyplot as plt
    out_path = Path(filename)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


__all__ = ["gantt_matplotlib"]


def gantt_matplotlib_inline(plan=None, start_date: Optional[date] = None, figsize=(10, 0.5), epic_only: bool = False):
    """Display a Gantt chart inline (Jupyter-friendly) and return (fig, ax).

    Does not write a file. Accepts same epic_only flag as gantt_matplotlib.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from IPython.display import display
    except ImportError as e:
        raise ImportError("matplotlib (and IPython for display) required for gantt_matplotlib_inline().") from e
    sched = _prepare_schedule(plan, start_date, epic_only)
    title = 'Plan Gantt (inline)' + (' [Epics]' if epic_only else '')
    min_start = min(s for _, s, _ in sched)
    max_end = max(e for _, _, e in sched)
    fig, ax = _plot_schedule(sched, figsize, title)
    return fig, ax

__all__.append("gantt_matplotlib_inline")
