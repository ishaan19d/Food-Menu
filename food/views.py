from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from .models import Item
from .forms import ItemForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    item_list = Item.objects.all()

    name=request.GET.get('name')
    if name!='' and name is not None:
        item_list=item_list.filter(item_name__icontains=name)

    paginator=Paginator(item_list,5)
    page=request.GET.get('page')
    item_list=paginator.get_page(page)
    return render(request, 'food/index.html', {'item_list': item_list})

class FoodDetail(DetailView):
    model=Item
    template_name='food/detail.html'
    context_object_name='item'

class CreateItem(CreateView):
    model = Item
    fields=['item_name','item_desc','item_price','item_image']
    template_name='food/item-form.html'

    def form_valid(self,form):
        form.instance.user_name=self.request.user
        return super().form_valid(form)

@login_required
def update_item(request,id):
    item = Item.objects.get(pk=id)
    form = ItemForm(request.POST or None,instance=item)
    if form.is_valid():
        form.save()
        return redirect('food:index')
    return render(request,'food/item-form.html',{'form':form,'item':item})

@login_required
def delete_item(request,id):
    item = Item.objects.get(pk=id)
    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    return render(request,'food/item-delete.html',{'item':item})
