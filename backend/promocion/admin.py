from django.contrib import admin
from promocion.models import Promocion, PromocionHorario, TipoPromocion

# Register your models here.
admin.site.register(TipoPromocion)
admin.site.register(Promocion)
admin.site.register(PromocionHorario)