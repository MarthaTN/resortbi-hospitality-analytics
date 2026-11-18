
from rest_framework.permissions import BasePermission


class _GroupPermission(BasePermission):
    group_names = ()

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.groups.filter(name__in=self.group_names).exists()
        )


class IsAdministrator(_GroupPermission):
    group_names = ("Administrator",)


class IsExecutive(_GroupPermission):
    group_names = ("Executive",)


class IsManager(_GroupPermission):
    group_names = ("Manager",)


class IsAnalyst(_GroupPermission):
    group_names = ("Analyst",)


class IsManagement(_GroupPermission):
    group_names = ("Administrator", "Executive", "Manager")


class IsAdministratorOrAnalyst(_GroupPermission):
    group_names = ("Administrator", "Analyst")


class IsAnalyticsUser(_GroupPermission):
    group_names = ("Administrator", "Executive", "Manager", "Analyst")
