from django_filters import FilterSet, ModelChoiceFilter, DateFilter, DateRangeFilter
from .models import Announcement, Category
from django import forms


class AnnouncementFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='categories__category_name',  # Исправлено на соответствие новой структуре
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Все категории',
    )

    date = DateFilter(
        field_name='announcement_date_time',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата',
        lookup_expr='date__gte',
    )

    date_range = DateRangeFilter(
        field_name='announcement_date_time',
        label='За период',
        empty_label='За весь период',
    )

    class Meta:
        model = Announcement
        fields = {
            'announcement_title': ['icontains'],
            'author': ['exact'],
            'announcement_date_time': ['gt'],
        }
