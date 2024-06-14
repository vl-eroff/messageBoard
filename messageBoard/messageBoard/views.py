from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Trade, Image
from .serializers import TradeSerializer


def trade_list_view(request):
    if request.method == 'GET':
        trades = Trade.objects.filter(status="open")
        trade_data = [trade.to_dict() for trade in trades]

        return JsonResponse(trade_data, safe=False)
    
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode())

            errors = {}
            if not json_data.get('title'):
                errors['title'] = 'Title is required'
            if not json_data.get('message'):
                errors['message'] = 'Message is required'
            if len(errors) > 0:
                return JsonResponse({'message': 'Invalid data', 'errors': errors}, status=400)

            title = json_data['title']
            message = json_data['message']
            status = 'open'

            if json_data.get('status'):
                status = json_data['status']

            current_user = None

            if request.user.is_authenticated:
                current_user = request.user

            trade = Trade.objects.create(
               title=title,
               message=message,
               status=status,
               author=current_user)
            
            trade_data = trade.to_dict()
            return JsonResponse(trade_data)
        
        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({'message': f'Invalid JSON data: {e}'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

def trade_detail_view(request, pk):
    if request.method == 'GET':
        try:
            trade = Trade.objects.get(pk=pk)
            trade_data = trade.to_dict()

            trade_data['image_urls'] = []
            for image in Image.objects.filter(trade=trade):
                image_url = image.image.path
                trade_data['image_urls'].append(image_url)

            return JsonResponse(trade_data)

        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Trade not found'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error retrieving trade: {e}'}, status=500)

    if request.method == "PUT":
        trade = get_object_or_404(Trade, pk=pk)
        data = request.data
        serializer = TradeSerializer(trade, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

#@login_required
def trade_delete_view(request, pk):
    trade = get_object_or_404(Trade, pk=pk)
    if request.method == "DELETE":
        trade.delete()
        return JsonResponse({"message": "Trade deleted successfully"}, status=204)
    return JsonResponse({"message": "Method not allowed"}, status=405)


#@login_required
def image_create_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({'message': 'Method not allowed'}, status=405)

    try:
        trade = get_object_or_404(Trade, pk=pk)

        if 'image' not in request.FILES:
            return JsonResponse({'message': 'Image file is required'}, status=400)

        image_file = request.FILES['image']

        if image_file.size > 1024 * 1024:  # 1MB limit
            return JsonResponse({'message': 'Image file size exceeds 1MB'}, status=400)
        if image_file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            return JsonResponse({'message': 'Unsupported image file type'}, status=400)

        Image.objects.create(trade=trade, image=image_file)

        return JsonResponse({'message': 'Image added successfully'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Trade not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Error creating image: {e}'}, status=500)

#@login_required
def image_delete_view(request, pk, image_pk):
    image = get_object_or_404(Image, pk=image_pk, trade__pk=pk)
    if request.method == "DELETE":
        image.delete()
        return JsonResponse({"message": "Image deleted successfully"}, status=204)
    return JsonResponse({"message": "Method not allowed"}, status=405)