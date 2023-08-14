# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Befriends(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, friend_id) found, that is not supported. The first column is selected.
    friend = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id', related_name='befriends_friend_set')

    class Meta:
        managed = False
        db_table = 'befriends'
        unique_together = (('user', 'friend'),)


class CommentReact(models.Model):
    reaction = models.CharField(max_length=10, blank=True, null=True)
    comment = models.ForeignKey('PostComment', models.DO_NOTHING)
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, comment_id) found, that is not supported. The first column is selected.

    class Meta:
        managed = False
        db_table = 'comment_react'
        unique_together = (('user', 'comment'),)


class CommentReply(models.Model):
    reply_id = models.FloatField(primary_key=True)
    media = models.ForeignKey('Media', models.DO_NOTHING, blank=True, null=True)
    comment = models.ForeignKey('PostComment', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id', blank=True, null=True)
    init_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment_reply'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EventHosting(models.Model):
    event = models.OneToOneField('Events', models.DO_NOTHING, primary_key=True)  # The composite primary key (event_id, user_id) found, that is not supported. The first column is selected.
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id')

    class Meta:
        managed = False
        db_table = 'event_hosting'
        unique_together = (('event', 'user'),)


class EventInterested(models.Model):
    event = models.OneToOneField('Events', models.DO_NOTHING, primary_key=True)  # The composite primary key (event_id, user_id) found, that is not supported. The first column is selected.
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id')

    class Meta:
        managed = False
        db_table = 'event_interested'
        unique_together = (('event', 'user'),)


class EventMedia(models.Model):
    event = models.OneToOneField('Events', models.DO_NOTHING, primary_key=True)  # The composite primary key (event_id, media_id) found, that is not supported. The first column is selected.
    media = models.ForeignKey('Media', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'event_media'
        unique_together = (('event', 'media'),)


class Events(models.Model):
    event_name = models.CharField(max_length=50, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    event_id = models.FloatField(primary_key=True)
    init_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'


class FriendReq(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, friend_req_id) found, that is not supported. The first column is selected.
    friend_req = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id', related_name='friendreq_friend_req_set')

    class Meta:
        managed = False
        db_table = 'friend_req'
        unique_together = (('user', 'friend_req'),)


class Marketplace(models.Model):
    product_name = models.CharField(max_length=50, blank=True, null=True)
    marketplace_id = models.FloatField(primary_key=True)
    price = models.FloatField(blank=True, null=True)
    init_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'marketplace'


class MarketplaceMedia(models.Model):
    marketplace = models.OneToOneField(Marketplace, models.DO_NOTHING, primary_key=True)  # The composite primary key (marketplace_id, media_id) found, that is not supported. The first column is selected.
    media = models.ForeignKey('Media', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'marketplace_media'
        unique_together = (('marketplace', 'media'),)


class MarketplaceOwning(models.Model):
    marketplace = models.OneToOneField(Marketplace, models.DO_NOTHING, primary_key=True)  # The composite primary key (marketplace_id, user_id) found, that is not supported. The first column is selected.
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id')

    class Meta:
        managed = False
        db_table = 'marketplace_owning'
        unique_together = (('marketplace', 'user'),)


class Media(models.Model):
    media_id = models.FloatField(primary_key=True)
    media_of = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'media'


class Message(models.Model):
    message_id = models.FloatField(primary_key=True)
    received_uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='received_uid', to_field='user_id', blank=True, null=True)
    sent_uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='sent_uid', to_field='user_id', related_name='message_sent_uid_set', blank=True, null=True)
    init_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message'


class MessageMedia(models.Model):
    message = models.OneToOneField(Message, models.DO_NOTHING, primary_key=True)  # The composite primary key (message_id, media_id) found, that is not supported. The first column is selected.
    media = models.ForeignKey(Media, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'message_media'
        unique_together = (('message', 'media'),)


class Page(models.Model):
    page_id = models.FloatField(primary_key=True)
    page_name = models.CharField(max_length=50, blank=True, null=True)
    page_type = models.CharField(max_length=20, blank=True, null=True)
    init_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page'


class PageLike(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, page_id) found, that is not supported. The first column is selected.
    page = models.ForeignKey(Page, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'page_like'
        unique_together = (('user', 'page'),)


class PageMedia(models.Model):
    page = models.OneToOneField(Page, models.DO_NOTHING, primary_key=True)  # The composite primary key (page_id, media_id) found, that is not supported. The first column is selected.
    media = models.ForeignKey(Media, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'page_media'
        unique_together = (('page', 'media'),)


class PageOwned(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, page_id) found, that is not supported. The first column is selected.
    page = models.ForeignKey(Page, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'page_owned'
        unique_together = (('user', 'page'),)


class Post(models.Model):
    post_id = models.FloatField(primary_key=True)
    post_type = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id', blank=True, null=True)
    init_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class PostComment(models.Model):
    comment_id = models.FloatField(primary_key=True)
    media = models.ForeignKey(Media, models.DO_NOTHING, blank=True, null=True)
    post = models.ForeignKey(Post, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id', blank=True, null=True)
    init_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_comment'


class PostDesc(models.Model):
    init_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_desc'


class PostInPage(models.Model):
    post = models.OneToOneField(Post, models.DO_NOTHING, primary_key=True)  # The composite primary key (post_id, page_id) found, that is not supported. The first column is selected.
    page = models.ForeignKey(Page, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_in_page'
        unique_together = (('post', 'page'),)


class PostMedia(models.Model):
    post = models.OneToOneField(Post, models.DO_NOTHING, primary_key=True)  # The composite primary key (post_id, media_id) found, that is not supported. The first column is selected.
    media = models.ForeignKey(Media, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_media'
        unique_together = (('post', 'media'),)


class PostReact(models.Model):
    post_reaction = models.CharField(max_length=10, blank=True, null=True)
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, post_id) found, that is not supported. The first column is selected.
    post = models.ForeignKey(Post, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_react'
        unique_together = (('user', 'post'),)


class PostSharedByUser(models.Model):
    share_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, to_field='user_id', blank=True, null=True)
    post = models.ForeignKey(Post, models.DO_NOTHING, blank=True, null=True)
    share_id = models.FloatField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'post_shared_by_user'


class PostSharedInPage(models.Model):
    post = models.OneToOneField(Post, models.DO_NOTHING, primary_key=True)  # The composite primary key (post_id, page_id) found, that is not supported. The first column is selected.
    page = models.ForeignKey(Page, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'post_shared_in_page'
        unique_together = (('post', 'page'),)


class ReplyReact(models.Model):
    reaction = models.CharField(max_length=10, blank=True, null=True)
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, reply_id) found, that is not supported. The first column is selected.
    reply = models.ForeignKey(CommentReply, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'reply_react'
        unique_together = (('user', 'reply'),)


class Settings(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    font_color = models.CharField(max_length=20, blank=True, null=True)
    text_color = models.CharField(max_length=20, blank=True, null=True)
    suggestions = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings'


class Users(models.Model):
    user_id = models.FloatField(unique=True, blank=True, null=True)
    user_name = models.CharField(primary_key=True, max_length=50)  # The composite primary key (user_name, mobile_number) found, that is not supported. The first column is selected.
    password = models.CharField(max_length=50, blank=True, null=True)
    mobile_number = models.CharField(max_length=20)
    profile_pic = models.CharField(max_length=100, blank=True, null=True)
    cover_photo = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        unique_together = (('user_name', 'mobile_number'),)
