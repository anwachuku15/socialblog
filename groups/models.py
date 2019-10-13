# GROUPS MODELS.PY FILE

from django.db import models
# Slugify - Convert spaces to hyphens, remove chars that aren't numbers/letters/underscores/hyphens. Convert to lowercase. Remove leading/trailing whitespace
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

# Link embedding
import misaka

# Returns the User model that is active in this project
from django.contrib.auth import get_user_model
# call things off of the current user session
User = get_user_model()

# Use custom template tags
from django import template
register = template.Library()


class Group(models.Model):
    # unique=True so there are no duplicate group names
    name = models.CharField(max_length=255,unique=True)
    # Slug generates a valid URL by using existing data
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=True,default='',blank=True)
    members = models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    # Saving a group upon creation
    def save(self,*args,**kwargs):
        # the slug URL will become self.name
        self.slug = slugify(self.name)
        # in case we have markdown(?) in the description
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    # After saving group, return to 'groups:single' template page
    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']

class GroupMember(models.Model):
    # Group member is related to the Group class (membership to a group)
    group = models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
    # connect GroupMember class to User and the Groups they belong to
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        # Every user is uniquely linked to a group
        unique_together = ('group','user')
