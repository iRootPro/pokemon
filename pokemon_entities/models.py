from django.db import models


class Pokemon(models.Model):
    title = models.TextField(verbose_name='Название на русском')
    title_en = models.CharField(
        verbose_name='Название на английском', max_length=50, blank=True)
    title_jp = models.CharField(
        verbose_name='Название на японском', max_length=50, blank=True)
    photo = models.ImageField(
        verbose_name='Фото', upload_to='photos', blank=True)
    description = models.TextField(verbose_name='Описание', default=' ')
    previous_evolution = models.ForeignKey('self', verbose_name='Из кого эволюционирует',
                                           null=True, blank=True,
                                           on_delete=models.SET_NULL, related_name='next_evolutions')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон', related_name='pokemons')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(verbose_name='Уровень', default=0)
    health = models.IntegerField(verbose_name='Здоровье', default=0)
    strenght = models.IntegerField(verbose_name='Сила', default=0)
    defence = models.IntegerField(verbose_name='Защита', default=0)
    stamina = models.IntegerField(verbose_name='Выносливость', default=0)
