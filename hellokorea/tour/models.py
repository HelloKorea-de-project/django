from django.db import models

class TourismServiceCategory(models.Model):
    contentTypeID = models.CharField(max_length=255, primary_key=True)
    mainCategory = models.CharField(max_length=255, null=False)
    subCategory1 = models.CharField(max_length=255, null=False)
    subCategory2 = models.CharField(max_length=255, null=False)

class SeoulAreaCode(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    korName = models.CharField(max_length=255, null=False)

class SeoulTourInfo(models.Model):
    contentID = models.CharField(max_length=255, primary_key=True)
    contentTypeID = models.ForeignKey(TourismServiceCategory, on_delete=models.CASCADE)
    siGunGuCode = models.ForeignKey(SeoulAreaCode, on_delete=models.CASCADE)
    addr = models.CharField(max_length=255, null=False)
    title = models.CharField(max_length=255, null=False)
    firstImage = models.CharField(max_length=255, null=True)
    la = models.FloatField(null=False)
    lo = models.FloatField(null=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    updatedAt = models.DateTimeField(auto_now=True, null=False)

class PerformancesFacilities(models.Model):
    mt10id = models.CharField(max_length=255, primary_key=True)
    fclynm = models.CharField(max_length=255, null=False)
    sidonm = models.CharField(max_length=255, null=False)
    gugunnm = models.CharField(max_length=255, null=False)
    adres = models.TextField(null=False)
    la = models.FloatField(null=False)
    lo = models.FloatField(null=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    updatedAt = models.DateTimeField(auto_now=True, null=False)

class Event(models.Model):
    mt20id = models.CharField(max_length=255, primary_key=True)
    mt10id = models.ForeignKey(PerformancesFacilities, on_delete=models.CASCADE)
    prfnm = models.CharField(max_length=255, null=False)
    eventStart = models.DateField(null=False)
    eventEnd = models.DateField(null=False)
    seatPrice = models.CharField(max_length=255, null=False)
    poster = models.TextField(null=True)
    genrenm = models.CharField(max_length=255, null=False)
    festival = models.CharField(max_length=1, null=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    updatedAt = models.DateTimeField(auto_now=True, null=False)

class Lodging(models.Model):
    mgtno = models.CharField(max_length=255, primary_key=True)
    rdnwhladdr = models.CharField(max_length=255, null=False)
    bplcnm = models.CharField(max_length=255, null=False)
    uptaenm = models.CharField(max_length=255, null=False)
    addCode = models.IntegerField(null=False)
    lo = models.FloatField(null=False)
    la = models.FloatField(null=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    updatedAt = models.DateTimeField(auto_now=True, null=False)