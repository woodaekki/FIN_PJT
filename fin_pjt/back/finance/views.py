# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer

@api_view(['POST'])
# 예금/적금 상품 데이터를 받아 DB에 저장 후 전체 상품 데이터 반환 
def save_products(request):
    data = request.data  

    for item in data:
        model_name = item.get('model')
        pk = item.get('pk')
        fields = item.get('fields', {})

        if model_name == 'finance.depositproducts':
            if not DepositProducts.objects.filter(fin_prdt_cd=pk).exists():
                DepositProducts.objects.create(
                    fin_prdt_cd=pk,
                    dcls_month=fields.get('dcls_month', ''),
                    fin_co_no=fields.get('fin_co_no', ''),
                    kor_co_nm=fields.get('kor_co_nm', ''),
                    fin_prdt_nm=fields.get('fin_prdt_nm', ''),
                    join_way=fields.get('join_way', ''),
                    mtrt_int=fields.get('mtrt_int', ''),
                    spcl_cnd=fields.get('spcl_cnd', ''),
                    join_deny=fields.get('join_deny', 1),
                    join_member=fields.get('join_member', ''),
                    etc_note=fields.get('etc_note', ''),
                    max_limit=fields.get('max_limit', '없음'),
                    dcls_strt_day=fields.get('dcls_strt_day', ''),
                    dcls_end_day=fields.get('dcls_end_day', ''),
                    fin_co_subm_day=fields.get('fin_co_subm_day', '')
                )

        elif model_name == 'finance.depositoptions':
            fin_prdt_cd = fields.get('fin_prdt_cd')
            if not DepositOptions.objects.filter(
                product__fin_prdt_cd=fin_prdt_cd,
                save_trm=fields.get('save_trm', 0),
                intr_rate_type_nm=fields.get('intr_rate_type_nm', '')
            ).exists():
                product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
                DepositOptions.objects.create(
                    product=product,
                    save_trm=fields.get('save_trm', 0),
                    intr_rate_type_nm=fields.get('intr_rate_type_nm', ''),
                    fin_prdt_cd=fin_prdt_cd,
                    intr_rate_type=fields.get('intr_rate_type', ''),
                    intr_rate=fields.get('intr_rate', -1),
                    intr_rate2=fields.get('intr_rate2', -1),
                )

        elif model_name == 'finance.savingproducts':
            if not SavingProducts.objects.filter(fin_prdt_cd=pk).exists():
                SavingProducts.objects.create(
                    fin_prdt_cd=pk,
                    dcls_month=fields.get('dcls_month', ''),
                    fin_co_no=fields.get('fin_co_no', ''),
                    kor_co_nm=fields.get('kor_co_nm', ''),
                    fin_prdt_nm=fields.get('fin_prdt_nm', ''),
                    join_way=fields.get('join_way', ''),
                    mtrt_int=fields.get('mtrt_int', ''),
                    spcl_cnd=fields.get('spcl_cnd', ''),
                    join_deny=fields.get('join_deny', 1),
                    join_member=fields.get('join_member', ''),
                    etc_note=fields.get('etc_note', ''),
                    max_limit=fields.get('max_limit', '없음'),
                    dcls_strt_day=fields.get('dcls_strt_day', ''),
                    dcls_end_day=fields.get('dcls_end_day', ''),
                    fin_co_subm_day=fields.get('fin_co_subm_day', '')
                )

        elif model_name == 'finance.savingoptions':
            fin_prdt_cd = fields.get('fin_prdt_cd')
            if not SavingOptions.objects.filter(
                product__fin_prdt_cd=fin_prdt_cd,
                save_trm=fields.get('save_trm', 0),
                intr_rate_type_nm=fields.get('intr_rate_type_nm', ''),
                rsrv_type=fields.get('rsrv_type', '')
            ).exists():
                product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
                SavingOptions.objects.create(
                    product=product,
                    save_trm=fields.get('save_trm', 0),
                    intr_rate_type_nm=fields.get('intr_rate_type_nm', ''),
                    fin_prdt_cd=fin_prdt_cd,
                    intr_rate_type=fields.get('intr_rate_type', ''),
                    rsrv_type=fields.get('rsrv_type', ''),
                    rsrv_type_nm=fields.get('rsrv_type_nm', ''),
                    intr_rate=fields.get('intr_rate', -1),
                    intr_rate2=fields.get('intr_rate2', -1),
                )

    deposit_products = DepositProducts.objects.all()
    saving_products = SavingProducts.objects.all()

    deposit_serializer = DepositProductsSerializer(deposit_products, many=True)
    saving_serializer = SavingProductsSerializer(saving_products, many=True)

    return Response({
        'deposit_products': deposit_serializer.data,
        'saving_products': saving_serializer.data,
        'message': 'DB 저장 완료 및 데이터 반환'
    })


@api_view(['GET'])
# 예금 상품 전체 목록 조회 
def deposit_products_list(request):
    deposits = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(deposits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# 예금 상품 개별 조회 
def deposit_product_detail(request, fin_prdt_cd):
    product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositProductsSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
# 예금 상품 옵션 전체 목록 조회 
def deposit_options_list(request):
    options = DepositOptions.objects.all()
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

# 특정 예금 옵션 상세 조회 
@api_view(['GET'])
def deposit_options_detail(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)  
    return Response(serializer.data)


@api_view(['GET'])
# 적금 상품 전체 목록 조회 
def saving_products_list(request):
    savings = SavingProducts.objects.all()
    serializer = SavingProductsSerializer(savings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# 적금 옵션 전체 목록 조회 
def saving_options_list(request):
    options = SavingOptions.objects.all()
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# 특정 적금 옵션 상세 조회
def saving_options_detail(request, fin_prdt_cd):
    options = SavingOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    if not options.exists():
        return Response({'error': 'Saving option not found'}, status=404)
    serializer = SavingOptionsSerializer(options.first())
    return Response(serializer.data)


@api_view(['GET'])
# 모든 예금 상품 코드 리스트 조회
def get_product_code(request):
    codes = DepositProducts.objects.values_list('fin_prdt_cd', flat=True)
    return Response(list(codes))
