from django.contrib import admin

from .models.attributes import Attribute, AttributeValue, VariantAttributeValue
from .models.catalogs import Brand, Category
from .models.images import ProductImage, ProductVariantImage
from .models.products import Product, ProductVariant

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(ProductVariantImage)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(VariantAttributeValue)
admin.site.register(Brand)
