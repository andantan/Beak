# -*- coding: utf-8 -*-

from abc import abstractmethod

from .metaclass import SingletonABCMeta


class QueueAbstractClass(SingletonABCMeta):
    @abstractmethod
    def allocate(self): pass
    
    
    @abstractmethod
    def is_allocated(self): pass
    
    
    @abstractmethod
    def enqueue(self): pass
    
    
    @abstractmethod
    def dequeue(self): pass
    
    
    @abstractmethod
    def reset(self): pass
    
    
    @abstractmethod
    def refresh(self): pass
    
    
    @abstractmethod
    def get_queue(self): pass
    
    
    @abstractmethod
    def get_count(self): pass
    
    
    @abstractmethod
    def overlook(self): pass
    
    
    @abstractmethod
    def exhale(self): pass