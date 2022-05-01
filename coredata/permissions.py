from rest_framework import permissions, status, exceptions


class PaidServicePermission(permissions.BasePermission):
    """
    Global permission check for paid service.
    """
    message = 'Ушбу вилоятга хисоблаш учун берилган лимит тугаган'
    status_code = status.HTTP_402_PAYMENT_REQUIRED

    def has_permission(self, request, view):
        if request.user.is_superuser is False:
            if request.user.region.limit is None:
                raise ServiceUnavailable
            if request.user.region.limit < 0 or request.user.region.limit == 0:
                raise ServiceUnavailable

        return True


class ServiceUnavailable(exceptions.APIException):
    status_code = 402
    default_detail = 'Ушбу вилоятга хисоблаш учун берилган лимит тугаган'
    default_code = 'Ушбу вилоятга хисоблаш учун берилган лимит тугаган'
