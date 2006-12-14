=================
plone.locking
=================

by Raphael Ritz, Jeff Roche, Martin Aspeli and others

Provides basic automatic locking support for Plone. Locks are stealable by
default, meaning that a user with edit privileges will be able to steal 
another user's lock, but will be warned that someone else may be editing
the same object.

Basic locking
-------------

By default, this is enabled on any ITTWLockable object. By default, this
applies to any Archetypes content object.

   >>> from Products.Archetypes.BaseContent import BaseContent
   >>> obj = BaseContent('id')
   >>> self.login('member1')

To lock this object, we adapt it to ILockable. The default adapter implements
locking using WebDAV locks.

   >>> from plone.locking.interfaces import ILockable
   >>> lockable = ILockable(obj)
   
To begin with, this object will not be locked:

   >>> lockable.locked()
   False

We can then lock it:

   >>> lockable.lock()
   >>> lockable.locked()
   True

If we try to lock it again, nothing happens.

   >>> lockable.lock()
   >>> lockable.locked()
   True

We can get information about the lock as well:

   >>> info = lockable.lock_info()
   >>> len(info)
   1
   >>> info[0]['time'] > 0
   True
   >>> info[0]['creator']
   'member1'

Once we have finished working on the object, we can unlock it.
   >>> lockable.unlock()
   >>> lockable.locked()
   False
   
There is no lock info when there is no lock:

    >>> lockable.lock_info()
    []

Stealable locks
---------------

By default, locks can be stolen. That is, if a particular user has a lock
and another user (with edit rights over the object) wants to edit the object,
the second user can unlock the object. This is opposed to "safe" unlocking,
which is done by the original owner.

Note that by convention, a user's own lock is "stealable" as well (kind of
like taking with the left hand and giving to the right).

    >>> lockable.lock()
    >>> lockable.can_safely_unlock()
    True
    >>> lockable.stealable()
    True
    
    >>> self.login('member2')
    
    >>> lockable.locked()
    True
    >>> lockable.can_safely_unlock()
    False
    >>> lockable.stealable()
    True
    
    >>> lockable.unlock()
    >>> lockable.locked()
    False
    
Unlocked objects are "stealable" and can be safely unlocked, since calling
unlock() on an unlocked object has no effect.
    
    >>> lockable.stealable()
    True
    >>> lockable.can_safely_unlock()
    True
    
However, an object can be marked as having a non-stealable lock

    >>> from plone.locking.interfaces import INonStealableLock
    >>> from zope.interface import directlyProvides
    >>> directlyProvides(obj, INonStealableLock)

    >>> lockable.lock()

The owner of the lock is of course free to unlock

    >>> lockable.stealable()
    True
    >>> lockable.unlock()
    >>> lockable.locked()
    False
    
Another user is not, and unlock() has no effect.

    >>> lockable.lock()
    >>> lockable.locked()
    True
    
    >>> self.login('member1')
    
    >>> lockable.stealable()
    False
    >>> lockable.unlock()
    >>> lockable.locked()
    True