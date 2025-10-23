from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer


class IsManagerOrOwner(permissions.BasePermission):
    """اجازه فقط برای مدیر یا خود فرد مسئول"""

    def has_object_permission(self, request, view, obj):
        # مدیرها همه رو ببینن
        if getattr(request.user, "role", None) == "manager":
            return True
        # کاربران فقط تسک‌های خودشون رو ببینن
        return obj.assignees.filter(id=request.user.id).exists()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrOwner]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "role", None) == "manager":
            return Task.objects.all()
        return Task.objects.filter(assignees=user)
