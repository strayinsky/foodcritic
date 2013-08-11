from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import logout
from django.views.generic import CreateView
from food.forms import RestaurantForm, DishForm, GradeForm, DishFormSet
from food.models import Restaurant, Dish, Grade
from django.utils import timezone
from django.forms.models import inlineformset_factory


class IndexView(generic.ListView):
    template_name = 'food/index.html'
    context_object_name = 'restaurant_list'

    def get_queryset(self):
        return Restaurant.objects.all()


class DetailView(generic.DetailView):
    template_name = 'food/detail.html'
    model = Restaurant


def grade(request, restaurant_id):
    dish_grades = request.POST.iteritems()
    u = request.user
    for key, value in dish_grades:
        if value and key.isdigit():
            print value[0]
            print value[1]
            d = Dish.objects.get(pk=key)
            g = Grade(user=u, dish=d, grade=value[0], comment=value[1], date=timezone.now())
            g.save()
    return HttpResponseRedirect(reverse('food:index'))


def addrestaurant(request):
    if request.method == 'POST': # If the form has been submitted...
        r = Restaurant(date=timezone.now(), user=request.user)
        form = RestaurantForm(request.POST, instance=r) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect(reverse('food:index')) # Redirect after POST
    else:
        form = RestaurantForm() # An unbound form

    return render(request, 'food/addrestaurant.html', {'form': form})


def editrestaurant(request, restaurant_id):
    to_edit = Restaurant.objects.get(pk=restaurant_id)
    #handles situation where user has entered valid data
    if request.method == 'POST':
        #creates a new form, pastes in the info from to_edit, including pk, then updates with changes from request.POST
        form = RestaurantForm(request.POST, instance=to_edit)
        if form.is_valid():
            new_restaurant = form.save(commit=False)
            #update the user and date
            new_restaurant.date = timezone.now()
            new_restaurant.user = request.user
            new_restaurant.save()
            return HttpResponseRedirect(reverse('food:index'))

    #handles situation either where nothing has been edited yet, or edited info was wrong
    form = RestaurantForm(instance=to_edit)

    return render(request, 'food/editrestaurant.html', {'form': form, 'restaurant_id': restaurant_id})


def adddish(request, restaurant_id):
    r = Restaurant.objects.get(pk=restaurant_id)
    print r.name
    if request.method == 'POST':
        d = Dish(date=timezone.now(), user=request.user, restaurant=r)
        form = DishForm(request.POST, instance=d)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('food:index'))
    else:
        form = DishForm()

    return render(request, 'food/adddish.html', {'form': form, 'restaurant': r})


def editdish(request, dish_id):
    to_edit = Dish.objects.get(pk=dish_id)
    #handles situation where user has entered valid data
    if request.method == 'POST':
        #creates a new form, pastes in the info from to_edit, including pk, then updates with changes from request.POST
        form = DishForm(request.POST, instance=to_edit)
        if form.is_valid():
            new_dish = form.save(commit=False)
            #update the user and date
            new_dish.date = timezone.now()
            new_dish.user = request.user
            new_dish.save()
            return HttpResponseRedirect(reverse('food:index'))

    #handles situation either where nothing has been edited yet, or edited info was wrong
    form = DishForm(instance=to_edit)

    return render(request, 'food/editdish.html', {'form': form, 'dish_id': dish_id})


class GradeDish(CreateView):
    form_class = GradeForm
    template_name = 'food/gradedish.html'

    #submitted data
    def post(self, request, **kwargs):
        dish_id = self.kwargs['dish_id']
        to_grade = Dish.objects.get(pk=dish_id)
        restaurant = to_grade.restaurant
        g = Grade(date=timezone.now(), user=request.user, dish=to_grade)
        form = GradeForm(request.POST, instance=g)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('food:detail', args=[restaurant.id]))
        else:
            form = GradeForm()
            return render(request, 'food/gradedish.html', {'form': form, 'dish': to_grade})

    #first time to the form
    def get(self, request, **kwargs):
        dish_id = self.kwargs['dish_id']
        to_grade = Dish.objects.get(pk=dish_id)
        print to_grade.name

        form = GradeForm()
        return render(request, 'food/gradedish.html', {'form': form, 'dish': to_grade})


class DishAndGrade(CreateView):
    def post(self, request, **kwargs):
        r = Restaurant.objects.get(pk=self.kwargs['pk'])
        print r.name
        print request.POST
        formset = DishFormSet(request.POST, instance=r, prefix='DISH')
        for i, form in enumerate(formset):
            form.grade = GradeForm(request.POST, prefix='GRADE_%s' % i)
        if formset.is_valid():
            for form in formset:
                if 'name' in form.cleaned_data:
                    dish = form.save(commit=False)
                    dish.user = request.user
                    dish.date = timezone.now()
                    grade = form.grade.save(commit=False)
                    grade.dish = dish
                    grade.user = request.user
                    grade.date = dish.date
                    dish.save()
                    grade.save()
            return HttpResponseRedirect(reverse('food:detail', args=[r.id]))
        else:
            return render(request, 'food/dishandgrade.html', {'dishes': formset, 'restaurant': r})

    def get(self, request, **kwargs):
        r = Restaurant.objects.get(pk=self.kwargs['pk'])
        formset = DishFormSet(prefix='DISH')
        return render(request, 'food/dishandgrade.html', {'dishes': formset, 'restaurant': r})
