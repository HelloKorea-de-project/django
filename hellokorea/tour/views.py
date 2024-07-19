from django.shortcuts import render

def index(request):
    return render(request, 'tour/index.html')

def district_detail(request, district_name):
    # 해당 구역의 상세 정보를 가져옵니다.
    context = {
        'district_name': district_name,
        # 필요하다면 다른 데이터도 추가
    }
    return render(request, 'tour/district_detail.html', context)