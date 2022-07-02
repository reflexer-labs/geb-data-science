# -*- python -*-
# -*- coding: utf-8 -*-
#
#  This file is part of the easydev software
#
#  Copyright (c) 2011-2017
#
#  File author(s): Thomas Cokelaer <cokelaer@gmail.com>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: https://github.com/cokelaer/easydev
#  Documentation: http://easydev-python.readthedocs.io
#
##############################################################################
import time
from multiprocessing import cpu_count, Process, Queue, Pool

__all__ = ["MultiProcessing"]


class MultiProcessing(object):
    """Class to run jobs in an asynchronous manner.

    You would use this class to run several jobs on a local computer that has
    several cpus.


    ::

        t = MultiProcessing(maxcpu=2)
        t.add_job(func, func_args)
        t.run()
        t.results[0] # contain returned object from the function *func*.


    .. warning:: the function must be a function, not a method. This is inherent
        to multiprocess in the multiprocessing module.

    .. warning:: the order in the results list may not be the same as the
        list of jobs. see :meth:`run` for details


    """

    def __init__(self, maxcpu=None, verbose=False, progress=True):
        """

        :param maxcpu: default returned by multiprocessing.cpu_count()
        :param verbose: print the output of each job. Could be very verbose
            so we advice to keep it False.
        :param progress: shows the progress


        """
        if maxcpu == None:
            maxcpu = cpu_count()

        self.maxcpu = maxcpu
        self.reset()
        self.verbose = verbose
        self.progress = progress

    def reset(self):
        """remove joves and results"""
        self.jobs = []  # a list of processes
        self.results = Queue()  # the results to append

    def add_job(self, func, *args, **kargs):
        """add a job in the pool"""
        if self.verbose:
            print(
                "Adding jobs in the queue..",
            )
        t = Process(target=func, args=args, kwargs=kargs)
        self.jobs.append(t)

    def _cb(self, results):
        if self.verbose is True:
            print("callback", results)
        if self.progress is True:
            self.pb.animate(len(self.results) + 1)
        self.results.append(results)

    def run(self, delay=0.1, verbose=True):
        """Run all the jobs in the Pool until all have finished.

        Jobs that have been added to the job list in :meth:`add_job`
        are now processed in this method by using a Pool. Here, we add
        all jobs using the apply_async method from multiprocess module.

        In order to ensure that the jobs are run sequentially in the same
        order as in :attr:`jobs`, we introduce a delay between 2 calls
        to apply_async (see http://docs.python.org/2/library/multiprocessing.html)

        A better way may be t use a Manager but for now, this works.

        """
        from easydev import Progress

        if self.progress is True:
            self.pb = Progress(len(self.jobs), 1)
            self.pb.animate(0)

        def init_worker():
            import signal

            signal.signal(signal.SIGINT, signal.SIG_IGN)

        self.results = []
        self.pool = Pool(self.maxcpu, init_worker)

        for process in self.jobs:
            self.pool.apply_async(
                process._target, process._args, process._kwargs, callback=self._cb
            )

            # ensure the results have same order as jobs
            # maybe important if you expect the order of the results to
            # be the same as inut; otherwise set delay to 0
            time.sleep(delay)

        try:
            while True:
                time.sleep(1)
                # check if all processes are finished.
                # if so, finished.
                count = len(self.results)
                if count == len(self.jobs):
                    break

        except KeyboardInterrupt:  # pragma: no cover
            print(
                "\nCaught interruption. " + "Terminating the Pool of processes... ",
            )
            self.pool.terminate()
            self.pool.join()
            print("... done")
        else:
            # Closing properly the pool
            self.pool.close()
            self.pool.join()

        # Pool cannot be pickled. So, if we want to pickel "MultiProcessing"
        # class itself, we must desctroy this instance
        del self.pool

        self.finished = True
