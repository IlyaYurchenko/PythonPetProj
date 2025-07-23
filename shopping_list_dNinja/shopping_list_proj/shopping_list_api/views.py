from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Product
from .schemas import ProductIn, ProductOut
from ninja.errors import HttpError
from typing import List
# Create your views here.

router = Router(tags=['Shopping List'])

@router.get('/items', response=List[ProductOut])
def get_all_products(request):
    products = Product.objects.all()
    return products

@router.get('/items/{product_id}', response=ProductOut)
def get_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    return product

@router.post('/items', response=ProductOut)
def create_product(request, product: ProductIn):
    try:
        product = Product.objects.create(**product.dict())
        return product
    except Exception as e:
        raise HttpError(400, detail=str(e), code=1001, message="Failed to create product")
    
@router.put('/items/{product_id}', response=ProductOut)
def update_product(request, product_id: int, product_in: ProductIn):
    product_obj = get_object_or_404(Product, id=product_id)
    for attr, value in product_in.dict(exclude_unset = True).items():
        setattr(product_obj, attr, value)
    product_obj.save()
    return f'{product_obj.name} has been updated successfully'

@router.delete('/items/{product_id}', response=ProductOut)
def delete_product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return {"detail": f"{product.name} has been deleted successfully", "code": 200, "message": "OK"}