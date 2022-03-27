from datetime import datetime
from tortoise import manager, models, fields


class SoftDeleteManager(manager.Manager):
    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(deleted_at=None)


class SoftDeleteMixin():
    deleted_at = fields.DatetimeField(default=None, null=True)
    
    class Meta:
        manager = SoftDeleteManager()

    async def delete(self):
        self.deleted_at = datetime.now()
        await self.save()

class TimeStampMixin():
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    

class BaseModel(models.Model):
    id = fields.IntField(pk=True)
    
    # class Meta:
    #     abstract = True