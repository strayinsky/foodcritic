import datetime
from haystack import indexes
from food.models import Restaurant, Dish


class DishIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Dish


class RestaurantIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    city = indexes.CharField(model_attr='city')
    country = indexes.CharField(model_attr='country')

    def get_model(self):
        return Restaurant
