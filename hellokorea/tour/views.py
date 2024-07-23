from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.db.models import Count


def index(request):
    return render(request, 'tour/index.html')

def district_detail(request, district_name):
    # Get unique main categories
    main_categories = TourismServiceCategory.objects.values_list('mainCategory', flat=True).distinct()
    
    # Get unique genres
    genres = Performances.objects.values_list('genrenm', flat=True).distinct()
    
    # Get unique lodging types
    lodging_types = Lodging.objects.values_list('uptaenm', flat=True).distinct()

    district_korName = SeoulAreaCode.objects.get(name=district_name).korName

    context = {
        'district_name': district_name,
        'district_korName': district_korName,
        'main_categories': main_categories,
        'genres': genres,
        'lodging_types': lodging_types
    }
    return render(request, 'tour/district_detail.html', context)

def get_district_info(request):
    # Fetch data for tourism, performance, and lodging
    tourism_data = SeoulTourInfo.objects.values('siGunGuCode__name', 'contentTypeID__subCategory1')\
                        .annotate(count=Count('contentID'))
    
    performance_data = PerformancesFacilities.objects.values('gugunnm')\
                            .annotate(count=Count('mt10id'))
    
    lodging_data = Lodging.objects.values('addCode')\
                    .annotate(count=Count('mgtno'))
    
    tourism_count = {}
    performance_count = {}
    lodging_count = {}
    
    for item in tourism_data:
        district_name = item['siGunGuCode__name']
        tourism_count[district_name] = tourism_count.get(district_name, 0) + item['count']
    
    for item in performance_data:
        try:
            district_name = SeoulAreaCode.objects.get(korName=item['gugunnm']).name
            performance_count[district_name] = item['count']
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
    max_performance = max(performance_count, key=performance_count.get)
    max_lodging = max(lodging_count, key=lodging_count.get)
    
    districts_info = {}
    for district in SeoulAreaCode.objects.all():
        name = district.name
        districts_info[name] = {
            'tourism': tourism_count.get(name, 0),
            'performance': performance_count.get(name, 0),
            'lodging_count': lodging_count.get(name, 0)
        }
    
    # Add the max information
    districts_info['max_tourism'] = max_tourism
    districts_info['max_performance'] = max_performance
    districts_info['max_lodging'] = max_lodging
    
    return JsonResponse(districts_info)

def get_district_detail(request, district_name):
    if request.method == "GET":
        # Fetch the SeoulAreaCode based on the district_name
        seoul_area_info = SeoulAreaCode.objects.get(name=district_name)
        area_code = seoul_area_info.code
        area_korName = seoul_area_info.korName

        # Fetch data based on district_name
        tour_infos = SeoulTourInfo.objects.filter(siGunGuCode__name=district_name).select_related('contentTypeID').values(
            'firstImage', 'title', 'contentTypeID__subCategory1', 'contentTypeID__subCategory2', 'addr', 'la', 'lo'
        )
        performances = Performances.objects.filter(mt10id__gugunnm=area_korName).values(
            'poster', 'prfnm', 'genrenm', 'prfpdfrom', 'prfpdto', 'pcseguidance', 'mt10id__adres', 'mt10id__la', 'mt10id__lo'
        )
        lodgings = Lodging.objects.filter(addCode=area_code).values(
            'mgtno', 'rdnwhladdr', 'bplcnm', 'uptaenm', 'lo', 'la'
        )

        # Convert querysets to list of dictionaries
        tour_infos = list(tour_infos)
        performances = list(performances)
        lodgings = list(lodgings)

        return JsonResponse({
            'tour_infos': tour_infos,
            'performances': performances,
            'lodgings': lodgings
        })
    
def get_tour_info(request, district_name):
    category = request.GET.get('category')
    tour_infos = SeoulTourInfo.objects.filter(siGunGuCode__name=district_name).select_related('contentTypeID').values(
        'firstImage', 'title', 'contentTypeID__subCategory1', 'contentTypeID__subCategory2', 'addr', 'la', 'lo'
    )
    if category:
        tour_infos = tour_infos.filter(contentTypeID__mainCategory=category)

    tour_infos = list(tour_infos)
    return JsonResponse({'tour_infos': tour_infos})

def get_performances(request, district_name):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    genre = request.GET.get('genre')

    area_korName = SeoulAreaCode.objects.get(name=district_name).korName
    
    performances = Performances.objects.filter(mt10id__gugunnm=area_korName).values(
        'poster', 'prfnm', 'genrenm', 'prfpdfrom', 'prfpdto', 'pcseguidance', 'mt10id__adres', 'mt10id__la', 'mt10id__lo'
    )
    if start_date and end_date:
        performances = performances.filter(prfpdfrom__lte=start_date, prfpdto__gte=end_date)
    elif start_date:
        performances = performances.filter(prfpdfrom__lte=start_date)
    elif end_date:
        performances = performances.filter(prfpdto__gte=end_date)
    if genre:
        performances = performances.filter(genrenm=genre)

    performances = list(performances)
    return JsonResponse({'performances': performances})

def get_lodgings(request, district_name):
    uptaenms = request.GET.get('uptaenms')

    # Fetch the SeoulAreaCode based on the district_name
    area_code = SeoulAreaCode.objects.get(name=district_name).code

    lodgings = Lodging.objects.filter(addCode=area_code).values(
        'mgtno', 'rdnwhladdr', 'bplcnm', 'uptaenm', 'lo', 'la'
    )
    if uptaenms:
        lodgings = lodgings.filter(uptaenm=uptaenms)

    lodgings = list(lodgings)
    return JsonResponse({'lodgings': lodgings})

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
#         tour_infos = SeoulTourInfo.objects.filter(siGunGuCode__name=district_name).select_related('contentTypeID').values(
#             'firstImage', 'title', 'contentTypeID__subCategory1', 'contentTypeID__subCategory2', 'addr', 'la', 'lo'
#         )
#         if category:
#             tour_infos = tour_infos.filter(contentTypeID__mainCategory=category)
        
#         performances = Performances.objects.filter(mt10id__gugunnm=district_name).values(
#             'poster', 'prfnm', 'genrenm', 'prfpdfrom', 'prfpdto', 'pcseguidance', 'mt10id__adres', 'mt10id__la', 'mt10id__lo'
#         )
#         if start_date and end_date:
#             performances = performances.filter(prfpdfrom__gte=start_date, prfpdto__lte=end_date)
#         if genre:
#             performances = performances.filter(genrenm=genre)

#         lodgings = Lodging.objects.filter(addCode=area_code).values(
#             'mgtno', 'rdnwhladdr', 'bplcnm', 'uptaenm', 'lo', 'la'
#         )
#         if uptaenms:
#             lodgings = lodgings.filter(uptaenm=uptaenms)

#         # Convert querysets to list of dictionaries
#         tour_infos = list(tour_infos)
#         performances = list(performances)
#         lodgings = list(lodgings)

#         return JsonResponse({
#             'tour_infos': tour_infos,
#             'performances': performances,
#             'lodgings': lodgings
#         })
