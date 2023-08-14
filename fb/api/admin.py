from django.contrib import admin

# Register your models here.
from .models import Users, Settings, ReplyReact, PostSharedInPage, PostSharedByUser, PostReact, PostMedia
from .models import PostInPage, PostDesc, PostComment, Post, PageOwned, PageMedia, PageLike, Page
from .models import MessageMedia, Message, Media, MarketplaceOwning, MarketplaceMedia, Marketplace
from .models import FriendReq, Events, EventMedia, EventHosting, EventInterested

admin.site.register(Users)
admin.site.register(Settings)
admin.site.register(ReplyReact)
admin.site.register(PostSharedInPage)
admin.site.register(PostSharedByUser)
admin.site.register(PostReact)
admin.site.register(PostMedia)
admin.site.register(PostInPage)
admin.site.register(PostDesc)
admin.site.register(PostComment)
admin.site.register(Post)
admin.site.register(PageOwned)
admin.site.register(PageMedia)
admin.site.register(PageLike)
admin.site.register(Page)
admin.site.register(MessageMedia)
admin.site.register(Message)
admin.site.register(Media)
admin.site.register(MarketplaceOwning)
admin.site.register(MarketplaceMedia)
admin.site.register(Marketplace)
admin.site.register(FriendReq)
admin.site.register(Events)
admin.site.register(EventMedia)
admin.site.register(EventHosting)
admin.site.register(EventInterested)