from zope.interface import implements
from zope.component import adapts

from AccessControl import getSecurityManager
from webdav.LockItem import LockItem

from plone.locking.interfaces import ILockable
from plone.locking.interfaces import INonStealableLock
from plone.locking.interfaces import ITTWLockable

class TTWLockable(object):
    """An object that is being locked through-the-web
    """
    
    implements(ILockable)
    adapts(ITTWLockable)

    def __init__(self, context):
        self.context = context

    def lock(self):
        if not self.locked():
            user = getSecurityManager().getUser()
            lock = LockItem(user)
            token = lock.getLockToken()
            self.context.wl_setLock(token, lock)

    def unlock(self):
        if self.locked() and self.stealable():
            self.context.wl_clearLocks()

    def locked(self):
        return bool(self.context.wl_isLocked())
    
    def can_safely_unlock(self):
        info = self.lock_info()
        
        # There is no lock, so return True
        if len(info) == 0:
            return True
            
        userid = getSecurityManager().getUser().getId()
        for l in info:
            # The current user is allowed to unlock
            if l['creator'] == userid:
                return True
        return False
        
    def stealable(self):
        # The lock is not non-stealable, so return True
        if not INonStealableLock.providedBy(self.context):
            return True
            
        # We can safely unlock anyway
        return self.can_safely_unlock()
        
    def lock_info(self):
        info = []
        for lock in self.context.wl_lockValues():
            if not lock.isValid():
                continue # Skip invalid/expired locks
            info.append({
                'creator' : lock.getCreator()[1],
                'time'    : lock.getModifiedTime(),
            })
        return info