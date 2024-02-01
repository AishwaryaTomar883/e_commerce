from django.contrib import admin

from utils.import_models import User, Category, Product, CarouselImage

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CarouselImage)
