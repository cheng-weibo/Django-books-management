from django.db import models


# Create your models here.


class Author(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    age = models.IntegerField()

    class Meta:
        unique_together = (
            ('name', 'age'),
        )


class Publisher(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    city = models.CharField(max_length=32)
    email = models.EmailField()


class Book(models.Model):
    bid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE)
    authors = models.ManyToManyField("Author", related_name='book2au')

    class Meta:
        unique_together = (
            ("title", "publisher"),
        )


# class Book2Author(models.Model):
#     b_id = models.ForeignKey("Book", on_delete=models.CASCADE)
#     a_id = models.ForeignKey("Author", on_delete=models.CASCADE)



