from django.db import models

# Create your models here.
class CustomPermission(models.Model):     
    class Meta:
        verbose_name_plural = "Custom Permission"
        permissions = (
             #For Case History --Starts
            ("can_add_case", "Can Add Case"),
            ("can_update_case", "Can Update Case"),
            ("can_add_follow_up", "Can Add Follow-up Case"),
            ("can_delete_follow_up", "Can Delete Follow-up Case"),
             #For Case History --Ends
        )