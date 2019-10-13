from django.contrib import admin
from . import models

# Register your models here.
# Used admin authentication for Group/GroupMember models

# Edit group members in group
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

admin.site.register(models.Group)
# because GroupMember is inline with Group, no need to register GroupMember
