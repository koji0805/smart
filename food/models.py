from django.db import models
from django.urls import reverse_lazy
from django.dispatch import receiver
import os

class BaseModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)  # 自動で作成時刻を記録
    update_at = models.DateTimeField(auto_now=True)  # 自動で更新時刻を記録

    class Meta:
        abstract = True  # これは抽象ベースクラスです

class PicturesManager(models.Manager):
    def filter_by_food(self, food):
        # 指定された食品に関連する画像をすべて返す
        return self.filter(food=food).all()

CATEGORY_CHOICES = (
('果物', '果物'),
('野菜', '野菜'),
('肉', '肉'),
('乳製品', '乳製品'),
('調味料', '調味料'),
('特殊調味料', '特殊調味料'),
('穀物類', '穀物類'),
('インスタント食品', 'インスタント食品'),
('お菓子', 'お菓子'),
('飲料', '飲料'),
('その他', 'その他'),
)

class Foods(BaseModel):
    name = models.CharField(max_length=255)
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='その他'  # 未分類のカテゴリをデフォルト値として設定
    )
    expirydate = models.DateField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'foods'

    def get_absolute_url(self):
        # 食品の詳細ページへのURLを返す
        return reverse_lazy("food:detail_food", kwargs={"pk": self.pk})

class PicturesManager(models.Manager):
  def filter_by_food(self, food):
    return self.filter(food=food).all
    

class Pictures(BaseModel):
    picture = models.ImageField(upload_to='pictures/')
    food = models.ForeignKey(Foods, on_delete=models.CASCADE, related_name="pictures")
    objects = PicturesManager()  # カスタムマネージャを使用

@receiver(models.signals.post_delete, sender=Pictures)
def delete_picture(sender, instance, **kwargs):
    # 画像ファイルが存在する場合は削除
    if instance.picture and os.path.isfile(instance.picture.path):
        os.remove(instance.picture.path)
