from django.db import models
from Accounts.models import User
from Courses.models import Course

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    is_successful = models.BooleanField(default=False)
    ref_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} - {self.course.title} - {'✅' if self.is_successful else '❌'}"
