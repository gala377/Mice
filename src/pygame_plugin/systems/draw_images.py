from ecs.system import GeneratorSystem, RunningSystem
from libmice.common.components import Transform
from libmice.autoregister import register

from pygame_plugin.components import Image, Window


@register
class DrawImages(GeneratorSystem):
    def __iter__(self) -> RunningSystem:
        window = self.resources.window[Window]
        yield None
        while True:
            drawable = zip(self.entity_storage[Image], self.entity_storage[Transform])
            drawable = filter(all, drawable)
            for img, trans in drawable:
                img.rect.center = (trans.x, trans.y)
                window.display.blit(img.img, img.rect)
            yield None
