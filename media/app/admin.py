from django.contrib import admin
from app.models import *

# Register your models here.
class VideoAdmin(admin.TabularInline):
    model=video
class HAdmin(admin.ModelAdmin):
    inlines=[VideoAdmin] 
class PaymentAdmin(admin.ModelAdmin):
    list_display=('id','order_id','payment_id','user','course','status')


admin.site.register(category,HAdmin)
admin.site.register(video)
admin.site.register(Userdetails)
admin.site.register(Usercourse)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Test)
admin.site.register(Certificate)
admin.site.register(Testsoulution)



