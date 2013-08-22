from django.forms import ModelForm
from django.utils import timezone
from django import forms
from haystack.forms import SearchForm, ModelSearchForm
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet
from food.models import Restaurant, Dish, Grade
from django.forms.models import inlineformset_factory, BaseInlineFormSet


class RestaurantForm(ModelForm):
    class Meta:
        model = Restaurant
        exclude = ('user', 'date')


class DishForm(ModelForm):
    class Meta:
        model = Dish
        exclude = ('user', 'date', 'restaurant')


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        exclude = ('user', 'date', 'dish')

    def is_valid(self):
        return True


class BaseDishFormset(BaseInlineFormSet):
    def is_valid(self):
        result = super(BaseDishFormset, self).is_valid()

        for form in self.forms:
            result = result and form.grade.is_valid()

        return result

    def save_new(self, form, commit=True):
        instance = super(BaseDishFormset, self).save_new(form, commit=commit)

        form.instance = instance
        if form.grade.is_valid():
            grade = form.grade.save(commit)
            grade.dish = instance

        return instance

    def add_fields(self, form, index):
        super(BaseDishFormset, self).add_fields(form, index)

        form.grade = GradeForm(prefix='GRADE_%s' % index)


DishFormSet = inlineformset_factory(Restaurant,
                                    Dish,
                                    formset=BaseDishFormset,
                                    max_num=3,
                                    can_delete=False,
                                    exclude=('user', 'date', 'restaurant'))


class CitySearchForm(SearchForm):
    city = forms.CharField(required=False)
    country = forms.CharField(required=False)

    # ModelSearchForm always uses get_models but if you don't specify the method,
    # then it gets all the models with indices
    def get_models(self):
        return [Restaurant]

    # the search method is also optional - writing out the method lets you customize it
    def search(self):
        # First, store the SearchQuerySet received from other processing.

        #sqs is a SearchQuerySet (we sould have called it anything)
        sqs = super(CitySearchForm, self).search().models(*self.get_models())

        if not self.is_valid():
            return self.no_query_found()

        # Check to see if a city was chosen.
        if self.cleaned_data['city']:
            sqs = sqs.filter(city=self.cleaned_data['city'])

        if self.cleaned_data['country']:
            sqs = sqs.filter(country=self.cleaned_data['country'])

        return sqs