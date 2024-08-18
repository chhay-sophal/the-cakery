from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import PartyAccessory

def view_all_accessories(request):
    accessories = PartyAccessory.objects.all()
    
    accessories_data = []
    for accessory in accessories:
        accessory_data = {
            'id': accessory.id,
            'name': accessory.name,
            'description': accessory.description,
            'price': float(accessory.price),
            'stock': accessory.stock,
            'created_at': accessory.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': accessory.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        accessories_data.append(accessory_data)

    context = {
        'accessories': accessories,
    }

    return JsonResponse(accessories_data, safe=False)

def get_accessory_details(request, item_id):
    accessory = get_object_or_404(PartyAccessory, pk=item_id)
    
    context = {
        'accessory': accessory,
    }

    return render(request, 'party_accessories/accessory_detail.html', context)
