""" Models for the blog app, representing the structure of the CMS database tables. """
from django.db import models

class PostStatusField(models.Field):
    """Custom Django model field to handle the enum_posts_status type from the CMS database."""
    description = "Custom field for enum_posts_status"

    def db_type(self, connection):
        return 'enum_posts_status'

    def get_prep_value(self, value):
        if value is None:
            return None
        return str(value)

# Create your models here.

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    hero_image = models.ForeignKey('Media', null=True,
                                      on_delete=models.SET_NULL, related_name='hero_image')
    content = models.JSONField(null=True)
    meta_title = models.CharField(max_length=255, null=True)
    meta_image = models.ForeignKey('Media', null=True,
                                      on_delete=models.SET_NULL, related_name='meta_image')
    meta_description = models.CharField(max_length=255, null=True)
    published_at = models.DateTimeField(null=True)
    generate_slug = models.BooleanField(default=True, null=True)
    slug = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    _status = PostStatusField(default='draft', null=True)

    objects: models.Manager["Post"] = models.Manager()
    # @ignore pylint: disable=missing-class-docstring
    class Meta:
        managed = False
        db_table = 'posts'
        

class Media(models.Model):
    id = models.AutoField(primary_key=True)
    alt = models.CharField(max_length=255, null=True)
    caption = models.JSONField(null=True)
    folder = models.ForeignKey('PayloadFolder', null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255, null=True)
    thumbnail_u_r_l = models.CharField(max_length=255, null=True)
    filename = models.CharField(max_length=255, null=True)
    mime_type = models.CharField(max_length=255, null=True)
    filesize = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    focal_x = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    focal_y = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_thumbnail_url = models.CharField(max_length=255, null=True)
    sizes_thumbnail_width = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_thumbnail_height = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_thumbnail_mime_type = models.CharField(max_length=255, null=True)
    sizes_thumbnail_filesize = models.DecimalField(max_digits=20, decimal_places=0,null=True)
    sizes_thumbnail_filename = models.CharField(max_length=255, null=True)
    sizes_square_url = models.CharField(max_length=255, null=True)
    sizes_square_width = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_square_height = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_square_mime_type = models.CharField(max_length=255, null=True)
    sizes_square_filesize = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    sizes_square_filename = models.CharField(max_length=255, null=True)
    sizes_small_url = models.CharField(max_length=255, null=True)
    sizes_small_width = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_small_height = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_small_mime_type = models.CharField(max_length=255, null=True)
    sizes_small_filesize = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    sizes_small_filename = models.CharField(max_length=255, null=True)
    sizes_medium_url = models.CharField(max_length=255, null=True)
    sizes_medium_width = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_medium_height = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_medium_mime_type = models.CharField(max_length=255, null=True)
    sizes_medium_filesize = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    sizes_medium_filename = models.CharField(max_length=255, null=True)
    sizes_large_url = models.CharField(max_length=255, null=True)
    sizes_large_width = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_large_height = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_large_mime_type = models.CharField(max_length=255, null=True)
    sizes_large_filesize = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    sizes_large_filename = models.CharField(max_length=255, null=True)
    sizes_xlarge_url = models.CharField(max_length=255, null=True)
    sizes_xlarge_width = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_xlarge_height = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_xlarge_mime_type = models.CharField(max_length=255, null=True)
    sizes_xlarge_filesize = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    sizes_xlarge_filename = models.CharField(max_length=255, null=True)
    sizes_og_url = models.CharField(max_length=255, null=True)
    sizes_og_width = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_og_height = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    sizes_og_mime_type = models.CharField(max_length=255, null=True)
    sizes_og_filesize = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    sizes_og_filename = models.CharField(max_length=255, null=True)

    objects: models.Manager["Media"] = models.Manager()
    # @ignore pylint: disable=missing-class-docstring
    class Meta:
        managed = False
        db_table = 'media'


class PayloadFolder(models.Model):
    """Model representing a folder for media items, as defined in the CMS database."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    folder_id = models.IntegerField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # @ignore pylint: disable=missing-class-docstring
    class Meta:
        managed = False
        db_table = 'payload_folders'
