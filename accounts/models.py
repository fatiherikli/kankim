# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from kankim.utils import here
from main.thumbs import ImageWithThumbsField


GENDER_CHOICES = (
    ('male', 'Bay'),
    ('female', 'Bayan')
)

COLOR_CHOICES = (
    ('#000', '#000'),
    ('#9C0', '#9C0'),
    ('#F69', '#F69'),
    ('#09F', '#09F'),
    ('#606', '#606'),
    ('#F03', '#F03'),
    ('brown', 'brown'),
    ('#F90', '#F90' ),
)

DEFAULT_COLOR = '#000'
THUMBNAIL_SIZES=(
    (125, 125),
    (220, 220)
)

class UserProfile(models.Model):
    #django user profili
    user = models.ForeignKey(User)

    # genel bilgiler
    color = models.CharField(max_length=10, verbose_name="Renk Düzeni", choices=COLOR_CHOICES) #renk duzeni
    birth_date = models.DateField(verbose_name="Doğum Tarihiniz", blank=True,  null=True)
    quotes = models.TextField(blank=True,null=True, verbose_name = "Sevdiğiniz Sözler")
    picture = ImageWithThumbsField(upload_to='uploads/', sizes=THUMBNAIL_SIZES, null=True, blank=True)

    #bilgeler
    current_location = models.CharField(max_length=50, verbose_name="Yaşadığınız Yer", blank=True,null=True)
    hometown = models.CharField(max_length=50, blank=True,null=True)

    #sevdikleri
    like_music = models.TextField(verbose_name="Yaşadığınız Yer", blank=True,null=True)
    like_movie = models.TextField(verbose_name="Sevdiğiniz Müzikler", blank=True,null=True)
    like_book = models.TextField(verbose_name="Sevdiğiniz Kitaplar",blank=True,null=True)

    #secilebilir ozellikler
    gender = models.CharField(choices = GENDER_CHOICES, verbose_name="Cinsiyetiniz", max_length='6', blank=True, null=True)

    def get_absolute_url(self):
        return "/%s" % self.user.username

    def friendship_list(self):
        return self.user.to_friend.filter(friendship_request=False)

    def dont_add(self):
        list = [self.user, ]
        for friend in self.user.to_friend.all():
            list.append(friend.from_friend)

        for friend in self.user.from_friend.all():
            list.append(friend.to_friend)

        return list

    def add_friend(self, to):
        if self.user == to:
            return False
        else:
            friendship, added = \
            Friendship.objects.get_or_create(from_friend=self.user, to_friend=to, friendship_request=True)

            if added:
                return True
            else:
                return friendship

    def friendship_requests(self):
        return self.user.to_friend.filter(friendship_request=True)

    def waiting_friendship_requests(self):
        return self.user.from_friend.filter(friendship_request=True)

    def accept_friendship_request(self,friendship):
        friendship.friendship_request=False
        friendship.save()
        Friendship(from_friend=self.user, to_friend=friendship.from_friend, friendship_request=False).save()


    def cancel_friendship_request(self,friendship):
        friendship.delete()


    def __unicode__(self):
        return self.user.username



class Friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name="from_friend")
    to_friend = models.ForeignKey(User, related_name="to_friend")
    friendship_request = models.BooleanField()

    def __unicode__(self):
        return "from: %s, to:%s" % (self.from_friend,self.to_friend)




def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)
