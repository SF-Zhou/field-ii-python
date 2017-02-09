import math
import functools
import threading
import matlab.engine
from . import MatlabEngine


class MatlabPool:
    def __init__(self, engine_count=2):
        session_names = matlab.engine.find_matlab()
        if len(session_names) < engine_count:
            raise EnvironmentError("Not Found Enough MATLAB Sessions! {0}/{1}"
                                   .format(len(session_names), engine_count))
        self.engines = list(map(MatlabEngine, session_names[:engine_count]))
        self.engine_count = engine_count

    @property
    def session_names(self):
        return [engine.session_name for engine in self.engines]

    def parallel(self, worker_factory, task: list, args: tuple=()):
        thread_pool = []
        worker_pool = []
        sub_task_count = math.ceil(len(task) / self.engine_count)
        for i, engine in enumerate(self.engines):
            sub_task = task[i * sub_task_count:(i + 1) * sub_task_count]
            worker = worker_factory(engine, sub_task)
            worker_pool.append(worker)

            thread = threading.Thread(target=worker.start, args=args)
            thread.start()
            thread_pool.append(thread)

        # wait for finishing
        for thread in thread_pool:
            thread.join()

        # concat when result is list
        if all(map(lambda w: isinstance(w.value, list), worker_pool)):
            return functools.reduce(lambda a, b: a + b, (worker.value for worker in worker_pool), [])
        else:
            return [worker.value for worker in worker_pool]
