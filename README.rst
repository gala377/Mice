=====================
Mice Game Framework
=====================

Welcome to **Mice**! **Mice** is an ECS Game Framework build
on top of pygame. 
It's still in early development and is a small
pet project rather than something that billions will use.


-----------------
Project structure
-----------------

As of now **Mice** is split into two packages:

- ``ecs`` which holds the heart of the entity component system.
- ``mice`` which is the framework with preconfigured systems, components and more.

-------------------
TODO
-------------------

Global
    - Keepachangelog.
    - Fix CI.

ECS
    - Components queries instead of pulling the world object.
    - Concurrent components looping.
    - Concurrent system execution.
    - Unit tests of ecs system.
    - Documentation of the ecs system.

Mice
    - Custom world object with common resources.
    - Documentation.
    - Unit tests.
