from django.db import models
from asgiref.sync import sync_to_async


class AsyncManager(models.Manager):
    async_get_func = sync_to_async(models.Manager.get)
    async_get_or_create_func = sync_to_async(models.Manager.get_or_create)
    async_count_func = sync_to_async(models.Manager.count)
    async_create_func = sync_to_async(models.Manager.create)
    async_last_func = sync_to_async(models.Manager.last)
    async_latest_func = sync_to_async(models.Manager.latest)

    @sync_to_async
    def async_first_func(self, *args, **kwargs):
        return self.filter(*args, **kwargs).first()

    async def get(self, *args, **kwargs):
        return await self.async_get_func(*args, **kwargs)

    async def get_or_create(self, *args, **kwargs):
        return await self.async_get_or_create_func(*args, **kwargs)

    async def count(self, *args, **kwargs):
        return await self.async_count_func(*args, **kwargs)

    async def create(self, *args, **kwargs):
        return await self.async_create_func(*args, **kwargs)

    async def first(self, *args, **kwargs):
        return await self.async_first_func(*args, **kwargs)

    async def last(self, *args, **kwargs):
        return await self.async_last_func(*args, **kwargs)

    async def latest(self, *args, **kwargs):
        return await self.async_latest_func(*args, **kwargs)

    async def filter(self, *args, **kwargs):
        return await sync_to_async(list)(self.filter(*args, **kwargs))

    async def all(self, *args, **kwargs):
        return await sync_to_async(list)(self.all())


class AsyncBaseModel(models.Model):
    objects = models.Manager()
    asyncs = AsyncManager()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    async def save(self, *args, **kwargs):
        return await sync_to_async(self.save)(*args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await sync_to_async(self.delete)(*args, **kwargs)

    class Meta:
        abstract = True


# class AsyncManager(models.Manager):

#     aget_func = sync_to_async(models.Manager.get)
#     aget_or_create_func = sync_to_async(models.Manager.get_or_create)
#     acount_func = sync_to_async(models.Manager.count)
#     acreate_func = sync_to_async(models.Manager.create)
#     alast_func = sync_to_async(models.Manager.last)
#     alatest_func = sync_to_async(models.Manager.latest)

#     async def aget(self, *args, **kwargs):
#         return await self.aget_func(*args, **kwargs)

#     async def aget_or_create(self, *args, **kwargs):
#         return await self.aget_or_create_func(*args, **kwargs)

#     async def acount(self, *args, **kwargs):
#         return await self.acount_func(*args, **kwargs)

#     async def acreate(self, *args, **kwargs):
#         return await self.acreate_func(*args, **kwargs)

#     @sync_to_async
#     def afirst_func(self, *args, **kwargs):
#         return self.filter(*args, **kwargs).first()

#     async def afirst(self, *args, **kwargs):
#         return await self.afirst_func(*args, **kwargs)

#     async def alast(self, *args, **kwargs):
#         return await self.alast_func(*args, **kwargs)

#     async def alatest(self, *args, **kwargs):
#         return await self.alatest_func(*args, **kwargs)

#     async def afilter(self, *args, **kwargs):
#         return await sync_to_async(list)(self.filter(*args, **kwargs))

#     async def aall(self, *args, **kwargs):
#         return await sync_to_async(list)(self.all())


# class AsyncMixin(models.Model):

#     objects: AsyncManager = AsyncManager()

#     async def asave(self, *args, **kwargs):
#         return await sync_to_async(self.save)(*args, **kwargs)

#     async def adelete(self, *args, **kwargs):
#         return await sync_to_async(self.delete)(*args, **kwargs)

#     class Meta:
#         abstract = True
