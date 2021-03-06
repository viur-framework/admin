import weakref
from typing import Any, Dict, List, Callable, Union
from weakref import ReferenceType

from PyQt5 import QtCore

"""
	Just a small EventDispatcher to distribute application-wide events.
"""


class WeakFuncWrapper:
	def __init__(self, targetFunc: Any):
		super(WeakFuncWrapper, self).__init__()
		self.targetFuncSelf: Union[ReferenceType[Any], None]
		if "__self__" in dir(targetFunc):
			self.targetFuncSelf = weakref.ref(targetFunc.__self__)
			self.targetFuncName = targetFunc.__name__
			self.targetFunc = None
		else:
			self.targetFuncSelf = None
			self.targetFuncName = None
			self.targetFunc = weakref.ref(targetFunc)

	def call(self, *args: Any, **kwargs: Any) -> None:
		if self.targetFuncName is not None and self.targetFuncSelf is not None:  # Bound function
			funcSelf = self.targetFuncSelf()
			if funcSelf is not None:
				getattr(funcSelf, self.targetFuncName)(*args, **kwargs)
		else:
			tf = self.targetFunc()
			if tf is not None:
				tf(*args, **kwargs)

	def isDead(self) -> bool:
		if self.targetFuncName is not None:  # Bound function
			return self.targetFuncSelf() is None
		else:
			return self.targetFunc() is None


class EventDispatcher(QtCore.QObject):
	"""
		Our global EventDispatcher.
		This is extended to allow registering events by priority.

		*Warning:* If connecting using connectWithPriority, its not guaranteed that you'll ever receive events.
		Its possible for objects earlier in the queue to stop distributing the event using StopIteration.
	"""
	highestPriority = 1
	highPriority = 2
	normalPriority = 3
	lowPriority = 4
	lowestPriority = 5
	eventMap: Dict[str, Any] = dict()

	def connectWithPriority(self, signal: str, func: Callable, priority: int) -> None:
		""" Connects the given function to the given event, using priority=#.

		:param signal:
		:param func:
		:param priority:
		:return:
		"""
		if signal not in EventDispatcher.eventMap:
			EventDispatcher.eventMap[signal] = {
				"high": list(),
				"normal": list(),
				"low": list()
			}
		obj = WeakFuncWrapper(func)
		if priority == self.highestPriority:  # Put this one first
			EventDispatcher.eventMap[signal]["high"].insert(0, obj)
		elif priority == self.highPriority:  # Append to "high"
			EventDispatcher.eventMap[signal]["high"].append(obj)
		elif priority == self.normalPriority:  # Append to "normal"
			EventDispatcher.eventMap[signal]["normal"].append(obj)
		elif priority == self.lowPriority:  # Prepend to "low"
			EventDispatcher.eventMap[signal]["low"].insert(0, obj)
		elif priority == self.lowestPriority:  # Append to "low"
			EventDispatcher.eventMap[signal]["low"].append(obj)

	def emit(self, signal: str, *args: Any) -> None:
		# super( EventDispatcher, self ).emit( signal, *args )
		if signal in EventDispatcher.eventMap:
			try:
				for e in EventDispatcher.eventMap[signal]["high"]:
					if e.isDead():
						EventDispatcher.eventMap[signal]["high"].remove(e)
					else:
						e.call(*args)
				for e in EventDispatcher.eventMap[signal]["normal"]:
					if e.isDead():
						EventDispatcher.eventMap[signal]["normal"].remove(e)
					else:
						e.call(*args)
				for e in EventDispatcher.eventMap[signal]["low"]:
					if e.isDead():
						EventDispatcher.eventMap[signal]["low"].remove(e)
					else:
						e.call(*args)
			except StopIteration:
				pass


event = EventDispatcher()
