from django.db import models


class TimestampFields(models.Model):
    '''
    abstract = True означает создание абстрактного класса
    Эта модель не будет использоваться для создания каких-либо таблиц базы данных.
    Вместо этого, когда он используется в качестве базового класса для других моделей,
    его поля будут добавлены к полям дочернего класса.
    '''
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Project(TimestampFields):
    """Объект на котором проводят измерения."""
    name = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Measurement(TimestampFields):
    """Измерение температуры на объекте."""
    value = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='measurements/static/images',
        height_field=None,
        width_field=None,
        max_length=10000,
        null=True
    )
