from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

CATEGORIES = [
    ('tank', 'Танки'),
    ('healer', 'Хилы'),
    ('dps', 'ДД'),
    ('trader', 'Торговцы'),
    ('guildmaster', 'Гилдмастеры'),
    ('questgiver', 'Квестгиверы'),
    ('blacksmith', 'Кузнецы'),
    ('leatherworker', 'Кожевники'),
    ('alchemist', 'Зельевары'),
    ('spellmaster', 'Мастера заклинаний'),
]


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.category_name


class Announcement(models.Model):
    announcement_date_time = models.DateTimeField(auto_now_add=True)
    announcement_title = models.CharField(max_length=255)
    announcement_text = RichTextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)  # Поле для категорий

    def preview(self):
        return self.announcement_text[:125] + '...'

    def __str__(self):
        return self.announcement_title


class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author} on {self.announcement}'


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Новый отклик на ваше объявление',
            f'Пользователь {instance.author} оставил отклик на ваше объявление "{instance.announcement}".',
            'from@example.com',
            [instance.announcement.author.author.email],
            fail_silently=False,
        )


@receiver(m2m_changed, sender=Announcement.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        categories = instance.categories.all()
        subscribers = set()
        for category in categories:
            subscribers.update(category.subscribers.all())

        emails = [user.email for user in subscribers]
        send_mail(
            subject=f'Новое объявление в категории {category}',
            message=f'В категории {category} появилось новое объявление: {instance.announcement_title}\n\n{instance.preview()}',
            from_email='from@example.com',
            recipient_list=emails,
            fail_silently=False,
        )

class AnnouncementCategory(models.Model):
    announcement = models.ForeignKey('Announcement', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('announcement', 'category')

    def __str__(self):
        return f'{self.announcement} in {self.category}'
