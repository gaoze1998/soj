import threading
import os
import pathlib
from datetime import datetime, timezone

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from soj.oj.models import User, Contest, Problem, Code, Grade
from soj.oj.permissions import IsLogined, IsContestOpen
from soj.oj.serializers import UserSerializer, ContestSerializer, ProblemSerializer, CodeSerializer
from soj.oj.utils.generate_location import generate_location
from soj.oj.utils.judge import judge, JudgeStatu


class Login(APIView):
    """
    User login.
    """
    def post(self, request):
        user_name = request.data["user_name"]
        password = request.data["password"]
        try:
            user = User.objects.get(user_name=user_name)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        user_dir = "./code/%s/" % (user_name)
        afile = pathlib.Path(user_dir)
        if not afile.is_dir():
            os.mkdir(user_dir)
        if not request.session.get("user_name", False) and user.password == password:
            request.session["user_name"] = user_name
            request.session.set_expiry(3000)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.session.get("user_name", False):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class Logout(APIView):
    """
    User logout.
    """
    permission_classes = [IsLogined]

    def post(self, request):
        request.session.pop("user_name")
        return Response(status=status.HTTP_200_OK)


class ContestList(generics.ListAPIView):
    """
    List all contests.
    """
    permission_classes = [IsLogined]

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


class ContestProblemsList(APIView):
    """
    List all contest's problems
    """
    permission_classes = [IsLogined and IsContestOpen]

    def get(self, request, pk):
        contest = Contest.objects.get(pk=pk)

        if contest.contest_start_time > datetime.now(tz=timezone.utc) \
                or contest.contest_end_time < datetime.now(tz=timezone.utc):
            return Response(status=status.HTTP_403_FORBIDDEN)

        problems = contest.problem_list.all()
        serializer = ProblemSerializer(problems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProblemDetail(generics.RetrieveAPIView):
    """
    Retrieve problem.
    """
    permission_classes = [IsLogined and IsContestOpen]

    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class task(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        judge(self.args[0], self.args[1])


class Submit(APIView):
    """
    submit the code.
    """
    permission_classes = [IsLogined and IsContestOpen]

    def post(self, request, contest_id, problem_id):
        code_raw = request.data["code"]
        contest = Contest.objects.get(pk=contest_id)
        problem = Problem.objects.get(pk=problem_id)
        user = User.objects.get(user_name=request.session["user_name"])

        try:
            code = Code.objects.get(contest=contest, problem=problem, user=user)
        except ObjectDoesNotExist:
            code = Code(contest=contest, problem=problem, user=user)
        language = request.data["language"]
        location = generate_location(request.session["user_name"], problem_id, language)
        code.code_location = location
        serializer = CodeSerializer(code)
        with open(location, "w") as code_file:
            code_file.write(code_raw)
        code.save()

        task_tread = task(args=(code, language))
        task_tread.start()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
