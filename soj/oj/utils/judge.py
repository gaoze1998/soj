import multiprocessing
import os
import ctypes
import pathlib
import resource
import sys
import time
from enum import Enum

from django.core.exceptions import ObjectDoesNotExist

from soj.oj.models import Grade
from soj.oj.utils.compare_output import compare_output


class JudgeStatu(Enum):
    OK = 0
    ERROR = 1


def judge_target(exec_file_location, sample_location, output_location, time_limit, memory_limit):
    prefix = "LD_PRELOAD=./libfakelib.so "

    resource.setrlimit(resource.RLIMIT_AS, (memory_limit * 1024 * 1024 + 256 * 1024 * 1024,
                                            memory_limit * 2 * 1024 * 1024 + 256 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CPU, (time_limit / 1000 + 2, time_limit / 1000 + 2))
    os.system("cat " + sample_location + " | " + prefix + exec_file_location + " > " + output_location)


def judge(code, language):
    try:
        grade = Grade.objects.get(problem=code.problem, contest=code.contest, user=code.user)
    except ObjectDoesNotExist:
        grade = Grade(problem=code.problem, contest=code.contest, user=code.user)
    grade.grade = 0

    problem = code.problem
    sample_location = problem.sample_location
    exec_file_location = ""

    time_limit = problem.problem_time_limit
    memory_limit = problem.problem_memory_limit

    if language == "C/C++":
        exec_file_location = code.code_location[:-4]

        exec_file = pathlib.Path(exec_file_location)
        if exec_file.is_file():
            os.remove(exec_file_location)

        ret = os.system("g++ -O2 %s -o %s" % (code.code_location, exec_file_location))
        if ret:
            grade.memo = "Error"
            grade.save()
            return
    elif language == "Java":
        exec_file_location = "java " + code.code_location
        time_limit = time_limit * 2
        memory_limit = memory_limit * 2

    elif language == "Python3":
        exec_file_location = "python3 " + code.code_location
        time_limit = time_limit * 5
        memory_limit = memory_limit * 5

    output_file = pathlib.Path(code.code_location + ".out")
    if output_file.is_file():
        os.remove(code.code_location + ".out")

    sum = 0
    for i in range(1, 2, 1):

        sample_location = sample_location + "%d.in" % i

        output_location = code.code_location + ".out"

        p = multiprocessing.Process(target=judge_target,
                                    args=(exec_file_location, sample_location, output_location, time_limit,
                                          memory_limit))
        p.start()
        p.join()
        res = p.exitcode

        sum += compare_output(str(output_location), str(sample_location))

    if res == JudgeStatu.ERROR:
        grade.memo = "Error"

    grade.grade = sum
    grade.memo = ""
    grade.save()

    return
