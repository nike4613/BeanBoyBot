import ctypes
import threading
import time

def async_raise(thread_obj, exception):
    """ Raises an exception inside an arbitrary active :class:`~threading.Thread`.
    Parameters
    ----------
    thread_obj : :class:`~threading.Thread`
        The target thread.
    exception : ``Exception``
        The exception class to be raised.
    Raises
    ------
    ValueError
        The specified :class:`~threading.Thread` is not active.
    SystemError
        The raise operation failed, the interpreter has been left in an inconsistent state.
    """
    target_tid = thread_obj.ident
    if target_tid not in {thread.ident for thread in threading.enumerate()}:
        raise ValueError('Invalid thread object, cannot find thread identity among currently active threads.')

    affected_count = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(target_tid), ctypes.py_object(exception))

    if affected_count == 0:
        raise ValueError('Invalid thread identity, no thread has been affected.')
    elif affected_count > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(target_tid), ctypes.c_long(0))
        raise SystemError("PyThreadState_SetAsyncExc failed, broke the interpreter state.")
