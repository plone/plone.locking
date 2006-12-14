from zope.interface import Interface

class ITTWLockable(Interface):
    """Marker interface for objects that are lockable through-the-web
    """
    
class INonStealableLock(Interface):
    """Mark an object with this interface to make locks be non-stealable.
    """
    
class ILockable(Interface):
    """A component that is lockable
    """

    def lock():
        """Lock the object
        """

    def unlock():
        """Unlock the object
        """
        
    def locked():
        """True if the object is locked
        """
        
    def can_safely_unlock():
        """Determine if the current user can safely unlock the object.
        
        That is, the object is either not locked, or it is locked by the
        current user.
        """
    
    def stealable():
        """Find out if the lock can be stolen
        """
    
    def lock_info():
        """Get information about locks on object. 
        
        Returns a list containing the following dict for each valid lock:
        
         - creator : the username of the lock creator
         - time    : the time at which the lock was acquired
        
        """