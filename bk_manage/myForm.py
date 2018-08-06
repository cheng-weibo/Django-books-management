from django import forms
from django.forms import widgets
from bk_manage import models


class BookFrom(forms.Form):
    title = forms.CharField(
        label='书名',
        max_length=32,
        error_messages={"required": "书名不能为空"},
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    publishDate = forms.DateField(
        label='出版日期',
        help_text="格式如：1990-1-1",
        error_messages={
            "required": "出版日期不能为空",
            "invalid": "日期不合法",
        },
        widget=widgets.DateTimeInput(attrs={"class": "form-control"})
    )
    price = forms.DecimalField(
        label='价格',
        max_digits=5, decimal_places=2,
        error_messages={"required": "价格不能为空", "invalid": "请输入数字"},
        widget=widgets.NumberInput(attrs={"class": "form-control"})
    )
    publisher = forms.ChoiceField(
        label='出版社',
        widget=widgets.Select(attrs={"class": "form-control"})
    )
    authors = forms.MultipleChoiceField(
        label='作者',
        error_messages={"required": "作者不能为空"},
        widget=widgets.SelectMultiple(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super(BookFrom, self).__init__(*args, **kwargs)
        self.fields['publisher'].choices = models.Publisher.objects.all().order_by('pid').values_list('pid', 'name')
        self.fields['authors'].choices = models.Author.objects.all().order_by('aid').values_list('aid', 'name')


class PublisherForm(forms.Form):
    name = forms.CharField(
        max_length=32,
        label='出版社',
        error_messages={"required": "出版社不能为空"},
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    city = forms.CharField(
        max_length=32,
        label='城市',
        error_messages={"required": "城市不能为空"},
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        max_length=32,
        label='邮箱',
        error_messages={"required": "邮箱不能为空", "invalid": "邮箱格式错误"},
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )


class AuthorForm(forms.Form):
    name = forms.CharField(
        max_length=32,
        label='姓名',
        error_messages={"required": "姓名不能为空"},
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    age = forms.IntegerField(
        label='年龄',
        error_messages={"required": "年龄不能为空", "invalid": "请输入数字"},
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
