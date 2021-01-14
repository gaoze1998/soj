from datetime import datetime, timezone

from rest_framework.permissions import BasePermission

from soj.oj.models import Contest


class IsLogined(BasePermission):
    def has_permission(self, request, view):
        print(view)
        return True if request.session.get("user_name", None) else False


class IsContestOpen(BasePermission):
    def has_permission(self, request, view):
        contest_id = view.kwargs["contest_id"]
        contest = Contest.objects.get(pk=contest_id)
        if contest.contest_start_time > datetime.now(tz=timezone.utc) \
                or contest.contest_end_time < datetime.now(tz=timezone.utc):
            return False
        return True
