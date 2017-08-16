from collections import namedtuple

from celery import shared_task

ReturnTuple = namedtuple('ReturnTuple', ['metajob', 'results'])


def _compat_return(metajob, *args):
    return ReturnTuple(metajob, args)


def extract_metajob(previous_task_results, *args):
    if isinstance(previous_task_results, ReturnTuple):
        return _compat_return(previous_task_results.metajob, *(previous_task_results.results + args))
    elif isinstance(previous_task_results, tuple):
        return _compat_return(previous_task_results[0], *(previous_task_results[1:] + args))
    return _compat_return(previous_task_results, *args)


# ==================================================
#   MONITORING TASKS
# ==================================================

@shared_task
def start(metajob):
    """
    Having a task for starting the job makes sure we measure the right time of running

    Parameters
    ----------
    metajob : MetaJob

    Returns
    -------
    MetaJob
    """
    metajob.start()
    return metajob


@shared_task
def stop(metajob, *args):
    """
    Having a task for stopping the job makes sure we measure the right time of completion (previous task is obviously
    done)

    Parameters
    ----------
    metajob : MetaJob or tuple
    args

    Returns
    -------
    MetaJob

    """
    metajob, args = extract_metajob(metajob, *args)
    metajob.stop()
    return _compat_return(metajob, *args)


# ==================================================
#   MAINTENANCE TASKS
# ==================================================

@shared_task
def remove_old_jobs(metajob, *args):
    """

    Parameters
    ----------
    metajob : MetaJob or tuple
    args

    Returns
    -------

    """
    metajob, args = extract_metajob(metajob, *args)
    from django.utils.timezone import now
    candidates = metajob.job.__class__.objects.filter(closure__lt=now())
    for candidate in candidates:
        candidate.delete()
    return _compat_return(metajob, *args)
