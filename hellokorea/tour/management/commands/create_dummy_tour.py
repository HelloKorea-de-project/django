import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tour.models import TourismServiceCategory, SeoulAreaCode, SeoulTourInfo, PerformancesFacilities, Performances, Lodging

class Command(BaseCommand):
    help = 'Create dummy data for the models'

    def handle(self, *args, **options):
        # Clear existing data
        TourismServiceCategory.objects.all().delete()
        SeoulAreaCode.objects.all().delete()
        SeoulTourInfo.objects.all().delete()
        PerformancesFacilities.objects.all().delete()
        Performances.objects.all().delete()
        Lodging.objects.all().delete()

        self.korean_area_names = {}
        self.create_tourism_service_categories()
        self.create_seoul_area_codes()
        self.create_seoul_tour_info()
        self.create_performances_facilities()
        self.create_performances()
        self.create_lodgings()
        self.stdout.write(self.style.SUCCESS('Successfully created dummy data'))

    def create_tourism_service_categories(self):
        categories = [
            ('1', 'Category1', 'SubCategory1-1', 'SubCategory2-1'),
            ('2', 'Category2', 'SubCategory1-2', 'SubCategory2-2'),
            ('3', 'Category3', 'SubCategory1-3', 'SubCategory2-3'),
        ]
        for contentTypeID, mainCategory, subCategory1, subCategory2 in categories:
            TourismServiceCategory.objects.get_or_create(
                contentTypeID=contentTypeID,
                mainCategory=mainCategory,
                subCategory1=subCategory1,
                subCategory2=subCategory2
            )

    def create_seoul_area_codes(self):
        areas = [
            (1, 'Jongno-gu', '종로구'),
            (2, 'Jung-gu', '중구'),
            (3, 'Yongsan-gu', '용산구'),
            (4, 'Seongdong-gu', '성동구'),
            (5, 'Gwangjin-gu', '광진구'),
            (6, 'Dongdaemun-gu', '동대문구'),
            (7, 'Jungnang-gu', '중랑구'),
            (8, 'Seongbuk-gu', '성북구'),
            (9, 'Gangbuk-gu', '강북구'),
            (10, 'Dobong-gu', '도봉구'),
            (11, 'Nowon-gu', '노원구'),
            (12, 'Eunpyeong-gu', '은평구'),
            (13, 'Seodaemun-gu', '서대문구'),
            (14, 'Mapo-gu', '마포구'),
            (15, 'Yangcheon-gu', '양천구'),
            (16, 'Gangseo-gu', '강서구'),
            (17, 'Guro-gu', '구로구'),
            (18, 'Geumcheon-gu', '금천구'),
            (19, 'Yeongdeungpo-gu', '영등포구'),
            (20, 'Dongjak-gu', '동작구'),
            (21, 'Gwanak-gu', '관악구'),
            (22, 'Seocho-gu', '서초구'),
            (23, 'Gangnam-gu', '강남구'),
            (24, 'Songpa-gu', '송파구'),
            (25, 'Gangdong-gu', '강동구'),
        ]
        for code, name, korean_name in areas:
            SeoulAreaCode.objects.get_or_create(code=code, name=name, korName=korean_name)
            self.korean_area_names[code] = korean_name

    def create_seoul_tour_info(self):
        tours = [
            ('1001', '1', 1, 'Address1', 'Title1', 'Image1', 37.5665, 126.9780),
            ('1002', '2', 2, 'Address2', 'Title2', 'Image2', 37.5651, 126.9895),
            ('1003', '3', 3, 'Address3', 'Title3', 'Image3', 37.5700, 126.9824),
        ]
        for contentID, contentTypeID, siGunGuCode, addr, title, firstImage, la, lo in tours:
            SeoulTourInfo.objects.get_or_create(
                contentID=contentID,
                contentTypeID=TourismServiceCategory.objects.get(contentTypeID=contentTypeID),
                siGunGuCode=SeoulAreaCode.objects.get(code=siGunGuCode),
                addr=addr,
                title=title,
                firstImage=firstImage,
                la=la,
                lo=lo
            )

    def create_performances_facilities(self):
        facilities = [
            ('P1', 'Facility1', 'Seoul', self.korean_area_names[1], 'Address1', 126.9780, 37.5665),
            ('P2', 'Facility2', 'Seoul', self.korean_area_names[2], 'Address2', 126.9895, 37.5651),
            ('P3', 'Facility3', 'Seoul', self.korean_area_names[3], 'Address3', 126.9824, 37.5700),
        ]
        for mt10id, fclynm, sidonm, gugunnm, adres, lo, la in facilities:
            PerformancesFacilities.objects.get_or_create(
                mt10id=mt10id,
                fclynm=fclynm,
                sidonm=sidonm,
                gugunnm=gugunnm,
                adres=adres,
                lo=lo,
                la=la
            )

    def create_performances(self):
        performances = [
            ('PRF1', 'P1', 'Performance1', timezone.now().date(), (timezone.now() + timedelta(days=10)).date(), '10000', 'Poster1', 'Genre1', 'Y'),
            ('PRF2', 'P2', 'Performance2', timezone.now().date(), (timezone.now() + timedelta(days=20)).date(), '20000', 'Poster2', 'Genre2', 'N'),
            ('PRF3', 'P3', 'Performance3', timezone.now().date(), (timezone.now() + timedelta(days=30)).date(), '30000', 'Poster3', 'Genre3', 'Y'),
        ]
        for mt20id, mt10id, prfnm, prfpdfrom, prfpdto, pcseguidance, poster, genrenm, festival in performances:
            Performances.objects.get_or_create(
                mt20id=mt20id,
                mt10id=PerformancesFacilities.objects.get(mt10id=mt10id),
                prfnm=prfnm,
                prfpdfrom=prfpdfrom,
                prfpdto=prfpdto,
                pcseguidance=pcseguidance,
                poster=poster,
                genrenm=genrenm,
                festival=festival
            )

    def create_lodgings(self):
        lodgings = [
            ('L1', 'Address1', 'Lodging1', 'Type1', 1, 126.9780, 37.5665),
            ('L2', 'Address2', 'Lodging2', 'Type2', 2, 126.9895, 37.5651),
            ('L3', 'Address3', 'Lodging3', 'Type3', 3, 126.9824, 37.5700),
        ]
        for mgtno, rdnwhladdr, bplcnm, uptaenm, addCode, lo, la in lodgings:
            Lodging.objects.get_or_create(
                mgtno=mgtno,
                rdnwhladdr=rdnwhladdr,
                bplcnm=bplcnm,
                uptaenm=uptaenm,
                addCode=addCode,
                lo=lo,
                la=la
            )