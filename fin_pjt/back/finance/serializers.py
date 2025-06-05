# serializer.py
from rest_framework import serializers
from django.db.models import Max
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions

# 예금 상품 
class DepositProductsSerializer(serializers.ModelSerializer):
    highest_rate = serializers.SerializerMethodField()
    class Meta:
        model = DepositProducts
        fields = ['fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'join_way', 'spcl_cnd', 'join_member', 'max_limit', 'mtrt_int', 'etc_note', 'highest_rate']
    def get_highest_rate(self, obj):
        return obj.depositoptions_set.aggregate(max_rate=Max('intr_rate2'))['max_rate']

# 예금 옵션 
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = ['fin_prdt_cd', 'intr_rate_type_nm', 'save_trm', 'intr_rate', 'intr_rate2']

# 적금 상품 
class SavingProductsSerializer(serializers.ModelSerializer):
    highest_rate = serializers.SerializerMethodField()
    class Meta:
        model = SavingProducts
        fields = ['fin_prdt_cd', 'fin_prdt_nm', 'kor_co_nm', 'max_limit', 'highest_rate']
    def get_highest_rate(self, obj):
        return obj.savingoptions_set.aggregate(max_rate=Max('intr_rate2'))['max_rate']

# 적금 옵션 
class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = ['fin_prdt_cd', 'intr_rate_type_nm', 'rsrv_type_nm', 'save_trm', 'intr_rate', 'intr_rate2']
