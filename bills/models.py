#------------------------------
# bills.models
#------------------------------
# Author: TangJianwei
# Create: 2019-07-07
#------------------------------
from django.db import models
from django.urls import reverse
from django.conf import settings


class Billym(models.Model):
    ''' 月账单
        以月份为单位，进行账单统计
    '''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)

    # 账单发生日期年份
    year  = models.PositiveIntegerField(null=False)
    # 账单发生日期月份
    month = models.PositiveIntegerField(null=False)

    class Meta:
        ordering = ('-year', '-month', )
        unique_together = ('owner', 'year', 'month', )
    
    def get_absolute_url(self):
        return reverse('bills:select_billym', args=[self.id, ])


class Bill(models.Model):
    ''' 日账单
        记录当天(或指定日期)的收入与支出
    '''
    billym = models.ForeignKey(Billym, on_delete=models.CASCADE)

    # 金额(7位整数，1位小数)
    money = models.DecimalField(max_digits=8, decimal_places=1, null=False)
    # 备注
    comment = models.TextField(max_length=32, null=False, blank=False)
    # 账单发生日期
    date = models.DateField(null=False)

    # 数据信息
    create_ts = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        ordering = ('-id', )

