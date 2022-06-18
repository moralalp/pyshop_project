from django import template

register = template.Library()


@register.filter()
def aktif_ve_stok(some_list):
    try:
        return some_list.filter(aktif=True, stok__gt=0)  # access the next element
    except:
        return None  # return empty string in case of exception


@register.filter()
def ileri(some_list, current_index):
    try:
        return some_list[int(current_index) + 1]  # access the next element
    except:
        return None  # return empty string in case of exception


@register.filter()
def geri(some_list, current_index):
    try:
        return some_list[int(current_index) - 1]  # access the previous element
    except:
        return None  # return empty string in case of exception
