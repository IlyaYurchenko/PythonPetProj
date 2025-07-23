from ninja import Schema, ModelSchema
from shopping_list_api.models import Product


class ProductIn(ModelSchema):
    class Meta:
        model = Product
        fields = '__all__'
        
class ProductOut(ModelSchema):
    id: int
    
    class Meta:
        model = Product
        fields = '__all__'

class ErrorResponse(Schema):
    detail: str
    code: int
    message: str
