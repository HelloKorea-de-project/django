from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.db.models import Count
import deepl
from django.conf import settings
import asyncio

translator = deepl.Translator(settings.DEEPL_API_KEY)
translate_dict = {}

def index(request):
    return render(request, 'tour/index.html')

def district_detail(request, district_name):
    # Get unique main categories
    main_categories = TourismServiceCategory.objects.values_list('mainCategory', flat=True).distinct()
    
    # Get unique genres
    genres = Event.objects.values_list('genrenm', flat=True).distinct()
    
    # Get unique lodging types
    lodging_types = Lodging.objects.values_list('uptaenm', flat=True).distinct()

    district_korName = SeoulAreaCode.objects.get(name=district_name).korName

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    translated_main_categories = loop.run_until_complete(asyncio.gather(*[translate_text(category) for category in main_categories]))
    translated_genres = loop.run_until_complete(asyncio.gather(*[translate_text(genre, field_name='genrenm') for genre in genres]))
    translated_lodging_types = loop.run_until_complete(asyncio.gather(*[translate_text(lodging_type, field_name='uptaenm') for lodging_type in lodging_types]))

    context = {
        'district_name': district_name,
        'district_korName': district_korName,
        'main_categories': translated_main_categories,
        'genres': translated_genres,
        'lodging_types': translated_lodging_types
    }
    return render(request, 'tour/district_detail.html', context)

def get_district_info(request):
    # Fetch data for tourism, event, and lodging
    tourism_data = SeoulTourInfo.objects.values('siGunGuCode__name', 'cat3__subCategory1')\
                        .annotate(count=Count('contentID'))
    
    event_data = PerformancesFacilities.objects.values('gugunnm')\
                            .annotate(count=Count('mt10id'))
    
    lodging_data = Lodging.objects.values('addCode')\
                    .annotate(count=Count('mgtno'))
    
    tourism_count = {}
    event_count = {}
    lodging_count = {}
    
    for item in tourism_data:
        district_name = item['siGunGuCode__name']
        tourism_count[district_name] = tourism_count.get(district_name, 0) + item['count']
    
    for item in event_data:
        try:
            district_name = SeoulAreaCode.objects.get(korName=item['gugunnm']).name
            event_count[district_name] = item['count']
        except SeoulAreaCode.DoesNotExist:
            continue
    
    for item in lodging_data:
        area_code = item['addCode']
        try:
            district_name = SeoulAreaCode.objects.get(code=area_code).name
            lodging_count[district_name] = item['count']
        except SeoulAreaCode.DoesNotExist:
            continue
    
    # Determine max counts
    max_tourism = max(tourism_count, key=tourism_count.get)
    max_event = max(event_count, key=event_count.get)
    max_lodging = max(lodging_count, key=lodging_count.get)
    
    districts_info = {}
    for district in SeoulAreaCode.objects.all():
        name = district.name
        districts_info[name] = {
            'tourism': tourism_count.get(name, 0),
            'event': event_count.get(name, 0),
            'lodging_count': lodging_count.get(name, 0)
        }
    
    # Add the max information
    districts_info['max_tourism'] = max_tourism
    districts_info['max_event'] = max_event
    districts_info['max_lodging'] = max_lodging
    
    return JsonResponse(districts_info)

def get_district_detail(request, district_name):
    if request.method == "GET":
        # Fetch the SeoulAreaCode based on the district_name
        seoul_area_info = SeoulAreaCode.objects.get(name=district_name)
        area_code = seoul_area_info.code
        area_korName = seoul_area_info.korName

        # Fetch data based on district_name
        tour_infos = SeoulTourInfo.objects.filter(siGunGuCode__name=district_name).select_related('cat3').values(
            'firstImage', 'title', 'cat3__subCategory1', 'cat3__subCategory2', 'addr', 'la', 'lo'
        )
        events = Event.objects.filter(mt10id__gugunnm=area_korName).values(
            'poster', 'prfnm', 'genrenm', 'eventStart', 'eventEnd', 'seatPrice', 'mt10id__adres', 'mt10id__la', 'mt10id__lo'
        )
        lodgings = Lodging.objects.filter(addCode=area_code).values(
            'mgtno', 'rdnwhladdr', 'bplcnm', 'uptaenm', 'lo', 'la'
        )

        # Convert querysets to list of dictionaries
        tour_infos = list(tour_infos)
        events = list(events)
        lodgings = list(lodgings)

        return JsonResponse({
            'tour_infos': tour_infos,
            'events': events,
            'lodgings': lodgings
        })
    
def get_tour_info(request, district_name):
    category = request.GET.get('category')
    tour_infos = SeoulTourInfo.objects.filter(siGunGuCode__name=district_name).select_related('cat3').values(
        'firstImage', 'title', 'cat3__subCategory1', 'cat3__subCategory2', 'addr', 'la', 'lo'
    )
    if category:
        tour_infos = tour_infos.filter(cat3__mainCategory=category)

    tour_infos = list(tour_infos)
    return JsonResponse({'tour_infos': tour_infos})

def get_events(request, district_name):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    genre = request.GET.get('genre')

    area_korName = SeoulAreaCode.objects.get(name=district_name).korName
    
    events = Event.objects.filter(mt10id__gugunnm=area_korName).values(
        'poster', 'prfnm', 'genrenm', 'eventStart', 'eventEnd', 'seatPrice', 'mt10id__adres', 'mt10id__la', 'mt10id__lo'
    )
    if start_date and end_date:
        events = events.filter(eventStart__lte=start_date, eventEnd__gte=end_date)
    elif start_date:
        events = events.filter(eventStart__lte=start_date)
    elif end_date:
        events = events.filter(eventEnd__gte=end_date)
    if genre:
        events = events.filter(genrenm=translate_dict[genre])

    events = list(events)

    async def translate_event(event):
        return {
            'poster': event['poster'],
            'prfnm': await translate_text(event['prfnm']),
            'genrenm': await translate_text(event['genrenm'], field_name='genrenm'),
            'eventStart': event['eventStart'],
            'eventEnd': event['eventEnd'],
            'seatPrice': await translate_text(event['seatPrice']),
            'mt10id__adres': await translate_text(event['mt10id__adres']),
            'mt10id__la': event['mt10id__la'],
            'mt10id__lo': event['mt10id__lo'],
        }

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    translated_events = loop.run_until_complete(asyncio.gather(*[translate_event(event) for event in events]))

    return JsonResponse({'events': translated_events})

def get_lodgings(request, district_name):
    uptaenm = request.GET.get('uptaenms')

    # Fetch the SeoulAreaCode based on the district_name
    area_code = SeoulAreaCode.objects.get(name=district_name).code

    lodgings = Lodging.objects.filter(addCode=area_code).values(
        'mgtno', 'rdnwhladdr', 'bplcnm', 'uptaenm', 'lo', 'la'
    )
    if uptaenm:
        lodgings = lodgings.filter(uptaenm=translate_dict[uptaenm])

    lodgings = list(lodgings)

    async def translate_lodging(lodging):
        return {
            'mgtno': lodging['mgtno'],
            'rdnwhladdr': await translate_text(lodging['rdnwhladdr']),
            'bplcnm': await translate_text(lodging['bplcnm']),
            'uptaenm': await translate_text(lodging['uptaenm'], field_name='uptaenm'),
            'lo': lodging['lo'],
            'la': lodging['la'],
        }
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    translated_lodgings = loop.run_until_complete(asyncio.gather(*[translate_lodging(lodging) for lodging in lodgings]))

    return JsonResponse({'lodgings': translated_lodgings})

async def translate_text(text, target_language='EN-US', field_name=None):
    result = translator.translate_text(text, target_lang=target_language)
    if field_name == 'uptaenm' or field_name == 'genrenm':
        translate_dict[result.text] = text
    return result.text

# def filter_data(request, district_name):
#     if request.method == "GET":
#         category = request.GET.get('category')
#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')
#         genre = request.GET.get('genre')
#         uptaenms = request.GET.get('uptaenms')

#         # Fetch the SeoulAreaCode based on the district_name
#         area_code = SeoulAreaCode.objects.get(name=district_name).code

#         # Fetch and filter data based on user inputs
#         tour_infos = SeoulTourInfo.objects.filter(siGunGuCode__name=district_name).select_related('cat3').values(
#             'firstImage', 'title', 'cat3__subCategory1', 'cat3__subCategory2', 'addr', 'la', 'lo'
#         )
#         if category:
#             tour_infos = tour_infos.filter(cat3__mainCategory=category)
        
#         events = events.objects.filter(mt10id__gugunnm=district_name).values(
#             'poster', 'prfnm', 'genrenm', 'eventStart', 'eventEnd', 'seatPrice', 'mt10id__adres', 'mt10id__la', 'mt10id__lo'
#         )
#         if start_date and end_date:
#             events = events.filter(eventStart__gte=start_date, eventEnd__lte=end_date)
#         if genre:
#             events = events.filter(genrenm=genre)

#         lodgings = Lodging.objects.filter(addCode=area_code).values(
#             'mgtno', 'rdnwhladdr', 'bplcnm', 'uptaenm', 'lo', 'la'
#         )
#         if uptaenms:
#             lodgings = lodgings.filter(uptaenm=uptaenms)

#         # Convert querysets to list of dictionaries
#         tour_infos = list(tour_infos)
#         events = list(events)
#         lodgings = list(lodgings)

#         return JsonResponse({
#             'tour_infos': tour_infos,
#             'events': events,
#             'lodgings': lodgings
#         })
