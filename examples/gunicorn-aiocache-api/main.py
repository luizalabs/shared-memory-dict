from aiocache import caches
from aiohttp import web


caches.set_config({
    'default': {
        'cache': 'shared_memory_dict.caches.aiocache.SharedMemoryCache',
        'name': 'sm'
    }
})


class Handler(web.View):

    async def get(self):
        key = self.request.query.get('key', '')
        text = await self.request.app['cache'].get(key)
        return web.Response(text=text)

    async def post(self):
        data = await self.request.post()
        await self.request.app['cache'].set(data['key'], data['value'])
        return web.Response(text='OK!')


async def app_shutdown(app):
    await app['cache'].close()


app = web.Application()
app.router.add_view('/', Handler)

app['cache'] = caches.get('default')
app.on_shutdown.append(app_shutdown)


if __name__ == '__main__':
    web.run_app(app)
