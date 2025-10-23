from django.db import models
from django.conf import settings

STATUS_CHOICES = [
    ("seen", "دیده شده"),
    ("working_on_it", "در حال انجام"),
    ("done", "انجام شده"),
]


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان تسک")
    description = models.TextField(verbose_name="توضیحات")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_tasks", verbose_name="ایجادکننده"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="assigned_tasks", verbose_name="افراد مسئول"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="seen", verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تسک"
        verbose_name_plural = "تسک‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
