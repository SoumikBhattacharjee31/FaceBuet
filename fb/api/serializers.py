from rest_framework.serializers import ModelSerializer
from .models import Users, Settings, ReplyReact, PostSharedInPage, PostSharedByUser, PostReact, PostMedia
from .models import PostInPage, PostDesc, PostComment, Post, PageOwned, PageMedia, PageLike, Page
from .models import MessageMedia, Message, Media, MarketplaceOwning, MarketplaceMedia, Marketplace
from .models import FriendReq, Events, EventMedia, EventHosting, EventInterested

class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
class SettingsSerializer(ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'
class ReplyReactSerializer(ModelSerializer):
    class Meta:
        model = ReplyReact
        fields = '__all__'
class PostSharedInPageSerializer(ModelSerializer):
    class Meta:
        model = PostSharedInPage
        fields = '__all__'
class PostSharedByUserSerializer(ModelSerializer):
    class Meta:
        model = PostSharedByUser
        fields = '__all__'
class PostReactSerializer(ModelSerializer):
    class Meta:
        model = PostReact
        fields = '__all__'
class PostMediaSerializer(ModelSerializer):
    class Meta:
        model = PostMedia
        fields = '__all__'
class PostInPageSerializer(ModelSerializer):
    class Meta:
        model = PostInPage
        fields = '__all__'
class PostDescSerializer(ModelSerializer):
    class Meta:
        model = PostDesc
        fields = '__all__'
class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
class PageOwnedSerializer(ModelSerializer):
    class Meta:
        model = PageOwned
        fields = '__all__'
class PageMediaSerializer(ModelSerializer):
    class Meta:
        model = PageMedia
        fields = '__all__'
class PageLikeSerializer(ModelSerializer):
    class Meta:
        model = PageLike
        fields = '__all__'
class PageSerializer(ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'
class MessageMediaSerializer(ModelSerializer):
    class Meta:
        model = MessageMedia
        fields = '__all__'
class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
class MarketplaceOwningSerializer(ModelSerializer):
    class Meta:
        model = MarketplaceOwning
        fields = '__all__'
class MarketplaceMediaSerializer(ModelSerializer):
    class Meta:
        model = MarketplaceMedia
        fields = '__all__'
class MarketplaceSerializer(ModelSerializer):
    class Meta:
        model = Marketplace
        fields = '__all__'
class FriendReqSerializer(ModelSerializer):
    class Meta:
        model = FriendReq
        fields = '__all__'
class EventsSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'
class EventMediaSerializer(ModelSerializer):
    class Meta:
        model = EventMedia
        fields = '__all__'
class EventHostingSerializer(ModelSerializer):
    class Meta:
        model = EventHosting
        fields = '__all__'
class EventInterestedSerializer(ModelSerializer):
    class Meta:
        model = EventInterested
        fields = '__all__'