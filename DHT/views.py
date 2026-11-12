from django.shortcuts import render
from django.db.models import Avg, Max, Min
from django.http import HttpResponse
from django.core.paginator import Paginator
import csv
from .models import Dht11

def dashboard(request):
    latest = Dht11.objects.order_by('-date').first()
    recent_readings = Dht11.objects.order_by('-date')[:50]
    total_count = Dht11.objects.count()
    alerts_count = Dht11.objects.filter(temperature__gt=25).count()
    
    stats = Dht11.objects.aggregate(
        avg_temp=Avg('temperature'),
        max_temp=Max('temperature'),
        min_temp=Min('temperature'),
        avg_hum=Avg('humidity'),
        max_hum=Max('humidity'),
        min_hum=Min('humidity')
    )
    
    context = {
        'latest': latest,
        'recent_readings': recent_readings,
        'total_count': total_count,
        'alerts_count': alerts_count,
        'stats': stats,
    }
    return render(request, 'DHT/dashboard.html', context)

def history(request):
    readings_list = Dht11.objects.order_by('-date')
    paginator = Paginator(readings_list, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_count': readings_list.count(),
        'alerts_count': Dht11.objects.filter(temperature__gt=25).count(),
    }
    return render(request, 'DHT/history.html', context)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="telemetry_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Temperature (°C)', 'Humidity (%)', 'Date & Time', 'Status'])
    
    for item in Dht11.objects.order_by('-date'):
        status = 'ALERT (>25°C)' if item.temperature > 25 else 'NORMAL'
        writer.writerow([item.id, item.temperature, item.humidity, item.date.strftime('%Y-%m-%d %H:%M:%S'), status])
        
    return response
