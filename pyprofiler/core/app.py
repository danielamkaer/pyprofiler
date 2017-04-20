import logging
logger = logging.getLogger(__name__)

import asyncio
import inspect
import pyprofiler.comm
from aiohttp import web

class ContainerInstance:
    def __init__(self, container, className, initType, factoryMethod, instance, *args):
        self.container = container
        self.className = className
        self.initType = initType
        self.factoryMethod = factoryMethod
        self.args = args
        self.instance = instance

    def resolveArgs(self):
        return [self.container[arg] for arg in self.args]

    def make(self):
        if self.initType == 'singleton':
            if self.instance == None:
                self.instance = self.factoryMethod(*self.resolveArgs())
                self.instance.container = self.container
                print(f"creating singleton: {self.className} = {self.instance}")
            return self.instance

        elif self.initType == 'factory':
            obj = self.factoryMethod(*self.resolveArgs())
            obj.container = self.container
            return obj
        
        elif self.initType == 'bind':
            return self.instance


class Container:
    def __init__(self):
        self.instances = {}

    def __getitem__(self, key):
        if key in self.instances:
            return self.instances[key].make()

        if inspect.isclass(key):
            logger.error(f'Autocreating type {key}.')
            return key()

    def bind(self, className, instance):
        self.instances[className] = ContainerInstance(self, className, 'bind', None, instance)

    def factory(self, className, factory, *args):
        self.instances[className] = ContainerInstance(self, className, 'factory', factory, None, *args)

    def singleton(self, className, factory, *args):
        self.instances[className] = ContainerInstance(self, className, 'singleton', factory, None, *args)

class Application(Container):
    def __init__(self, argv):
        super().__init__()
        self.argv = argv
        self.bind(asyncio.BaseEventLoop, asyncio.get_event_loop())

        self.boot = []

    def register(self, className):
        className.register(self)
        self.boot.append(className)

    def run_coroutine(self, coroutine):
        self[asyncio.BaseEventLoop].call_soon(lambda: asyncio.ensure_future(coroutine))

    def run(self):
        for className in self.boot:
            self[className].boot()
#        app = web.Application(loop=self[asyncio.BaseEventLoop])
#        self[web.Application] = app
#
#        app.router.add_static('/node_modules', path='node_modules', name='node_modules')
#        app.router.add_static('/', path='pyprofiler/public', name='static')
#
        print(f"run_app({self[web.Application]})")

        app = self[web.Application]
        handler = app.make_handler()
        loop = self[asyncio.BaseEventLoop]
        loop.run_until_complete(app.startup())
        server = loop.run_until_complete(loop.create_server(handler, '127.0.0.1', 8080, backlog=128))

        try:
            #web.run_app(self[web.Application], host='127.0.0.1', port=8080)
            loop.run_forever()
        except KeyboardInterrupt:
            print("Keyboard Interrupt")

        for className in self.boot:
            o = self[className]
            if hasattr(o, 'shutdown') and callable(getattr(o, 'shutdown')):
                if asyncio.iscoroutinefunction(o.shutdown):
                    loop.run_until_complete(o.shutdown())
                else:
                    o.shutdown()

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.run_until_complete(app.shutdown())
        loop.run_until_complete(handler.shutdown())
        loop.run_until_complete(app.cleanup())

        loop.close()

class WebApplication:

    def __init__(self, app):
        self.app = app

    @staticmethod
    def register(app):
        app.singleton(web.Application, lambda loop: web.Application(loop=loop), asyncio.BaseEventLoop)
        app.singleton(WebApplication, WebApplication, web.Application)

    def boot(self):
        print(f"WebApplication booted app={self.app}")
        self.app.router.add_static('/node_modules', path='node_modules', name='node_modules')
        self.app.router.add_static('/static', path='pyprofiler/public', name='static')
