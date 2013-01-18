# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from event import event
from utils import RegisterQueue, Overlay, formatString
from ui.relationalselectionUI import Ui_relationalSelector
from handler.tree import TreeList
from ui.treeselectorUI import Ui_TreeSelector
from os import path
from bones.relational import RelationalViewBoneDelegate
from widgets.tree import TreeWidget, TreeItem, DirItem

class TreeItemViewBoneDelegate( RelationalViewBoneDelegate ):
	pass

class TreeItemEditBone( QtGui.QWidget ):
	def __init__(self, modulName, boneName, skelStructure, *args, **kwargs ):
		super( TreeItemEditBone,  self ).__init__( *args, **kwargs )
		self.skelStructure = skelStructure
		self.modulName = modulName
		self.boneName = boneName
		self.toModul = self.skelStructure[ self.boneName ]["type"].split(".")[1]
		self.format = "$(name)"
		if "format" in skelStructure[ boneName ].keys():
			self.format = skelStructure[ boneName ]["format"]
		self.layout = QtGui.QHBoxLayout( self )
		self.addBtn = QtGui.QPushButton( QtCore.QCoreApplication.translate("TreeItemEditBone", "Select"), parent=self )
		iconadd = QtGui.QIcon()
		iconadd.addPixmap(QtGui.QPixmap("icons/actions/relationalselect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.addBtn.setIcon(iconadd)
		self.addBtn.connect( self.addBtn, QtCore.SIGNAL('released()'), self.on_addBtn_released )
		self.layout.addWidget( self.addBtn )
		if not skelStructure[boneName]["multiple"]:
			self.entry = QtGui.QLineEdit( self )
			self.entry.setReadOnly(True)
			self.layout.addWidget( self.entry )
			icon6 = QtGui.QIcon()
			icon6.addPixmap(QtGui.QPixmap("icons/actions/relationaldeselect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.delBtn = QtGui.QPushButton( "", parent=self )
			self.delBtn.setIcon(icon6)
			self.layout.addWidget( self.delBtn )
			self.delBtn.connect( self.delBtn, QtCore.SIGNAL('released()'), self.on_delBtn_released )
			self.selection = None
		else:
			self.selection = []

	def setSelection(self, selection):
		if self.skelStructure[self.boneName]["multiple"]:
			self.selection = selection
		elif len( selection )>0 :
			self.selection = selection[0]
			self.entry.setText( formatString( self.format, self.selection ) )
		else:
			self.selection = None
	
	def on_addBtn_released(self, *args, **kwargs ):
		queue = RegisterQueue()
		event.emit( QtCore.SIGNAL('requestTreeItemBoneSelection(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject,PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), queue, self.modulName, self.boneName, self.skelStructure, self.selection, self.setSelection )
		self.widget = queue.getBest()()

	def on_delBtn_released(self, *args, **kwargs ):
		if self.skelStructure[ self.boneName ]["multiple"]:
			self.selection = []
		else:
			self.selection = None
			self.entry.setText("")

	def unserialize( self, data ):
		if not self.boneName in data.keys():
			return
		self.selection = data[ self.boneName ]
		if not self.skelStructure[self.boneName]["multiple"]:
			self.entry.setText( formatString( self.format, data[ self.boneName ] ) )

	def serialize(self):
		if self.selection:
			if not self.skelStructure[self.boneName]["multiple"]:
				return( str( self.selection["id"] ) )
			else:
				return( [ str( x["id"] ) for x in self.selection ] )
		else:
			return( None )
	
	def serializeForDocument(self):
		if self.selection:
			if not self.skelStructure[self.boneName]["multiple"]:
				return( str( self.selection ) )
			else:
				return( [ x for x in self.selection ] )
		else:
			return( None )

class SelectedListWidget( QtGui.QListWidget ):
	def __init__(self, parent, modul, selection=None, treeItem=None, dragSource=None, *args, **kwargs ):
		super( SelectedListWidget, self ).__init__( *args, **kwargs )
		self.selection = selection or []
		self.treeItem = treeItem
		self.dragSource = dragSource
		for s in selection:
			self.addItem( self.treeItem( s ) )
		self.setAcceptDrops( True )
		self.connect( self, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), self.itemDoubleClicked )
	
	def itemDoubleClicked(self, item):
		self.takeItem( self.indexFromItem( item ).row() )
		self.selection.remove( item.data )
		self.clear()
		for s in self.selection:
			self.addItem( self.treeItem( s ) )

	def dropEvent(self, event):
		if event.source()==self.dragSource:
			if not self.selection:
				self.selection = []
			for item in self.dragSource.selectedItems():
				if item.data in self.selection:
					continue
				self.extend( [item.data] )

	def set(self, selection):
		self.clear()
		self.selection = selection
		for s in selection:
			self.addItem( self.treeItem( s ) )
	
	def extend(self, selection):
		self.selection += selection
		for s in selection:
			self.addItem( self.treeItem( s ) )
	
	def get(self):
		return( self.selection )

	def dragMoveEvent(self, event):
		event.accept()

	def dragEnterEvent(self, event):
		event.accept()
	
	def keyPressEvent( self, e ):
		if e.matches( QtGui.QKeySequence.Delete ):
			for item in self.selectedItems():
				self.takeItem( self.indexFromItem( item ).row() )
				self.selection.remove( item.data )
		else:
			super( SelectedListWidget, self ).keyPressEvent( e )

class BaseTreeItemBoneSelector( QtGui.QWidget ):
	treeItem = None #Allow override of these on class level
	dirItem = None
	
	def __init__(self, modulName, boneName, skelStructure, selection, setSelection, parent=None, widget=None, *args, **kwargs ):
		super( BaseTreeItemBoneSelector, self ).__init__( parent, *args, **kwargs )
		self.modul = skelStructure[ boneName ]["type"].split(".")[1]
		self.boneName = boneName
		self.skelStructure = skelStructure
		self.setSelection = setSelection
		self.multiple = skelStructure[boneName]["multiple"]
		self.ui = Ui_TreeSelector()
		self.ui.setupUi( self )
		layout = QtGui.QHBoxLayout( self.ui.listWidget )
		self.ui.listWidget.setLayout( layout )
		if not widget:
			widget = TreeWidget
		self.tree = widget( self.ui.listWidget, self.modul, None, None, treeItem=self.treeItem, dirItem=self.dirItem )
		layout.addWidget( self.tree )
		self.tree.show()
		layout = QtGui.QHBoxLayout( self.ui.listSelected )
		self.ui.listSelected.setLayout( layout )
		self.selected = SelectedListWidget( self.ui.listSelected, self.modul, selection=selection, treeItem=self.treeItem, dragSource=self.tree )
		layout.addWidget( self.selected )
		self.selected.show()
		#self.toolBar = QtGui.QToolBar( self.ui.wdgActions )
		#self.toolBar.setIconSize( QtCore.QSize( 32, 32 ) )
		#self.ui.boxActions.insertWidget( 0, self.toolBar )
		#queue = RegisterQueue()
		#event.emit( QtCore.SIGNAL('requestTreeModulActions(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), queue, self.modul, self )
		#for item in queue.getAll():
		#	i = item( self )
		#	if isinstance( i, QtGui.QAction ):
		#		self.toolBar.addAction( i )
		#		self.ui.listWidget.addAction( i )
		#	else:
		#		self.toolBar.addWidget( i )
		self.ui.listSelected.setAcceptDrops( True )
		#self.clipboard = None  #(str repo,str path, bool doMove, list treeItems, list dirs )
		if not self.multiple:
			self.ui.listSelected.hide()
			self.ui.lblSelected.hide()
			self.ui.btnAddSelected.hide()
		else:
			if selection:
				for sel in selection:
					self.selected.extend( [sel] )
		#self.ui.listSelected.keyPressEvent = self.on_listSelection_event
		#self.ui.listSelected.dragEnterEvent = self.onDragEnterEvent
		#self.ui.listSelected.dragMoveEvent = self.onDragMoveEvent
		#self.ui.listSelected.dropEvent = self.onDropEvent
		
		
		#self.delShortcut = QtGui.QShortcut( self.ui.listSelected )
		#self.delShortcut.setContext( QtCore.Qt.WidgetWithChildrenShortcut )
		#self.delShortcut.setKey( QtGui.QKeySequence.Delete )
		#self.connect( self.delShortcut, QtCore.SIGNAL("activated()"), self.onDeleteCurrentSelection )
		event.emit( QtCore.SIGNAL('stackWidget(PyQt_PyObject)'), self )
		self.connect( self.tree, QtCore.SIGNAL("itemDoubleClicked(PyQt_PyObject)"), self.on_listWidget_itemDoubleClicked)

	def on_cbRootNode_currentIndexChanged( self, text ): #Fixme: currently disabled
		if not isinstance( text, str ):
			return
		for repo in self.rootNodes:
			if repo["name"] == text:
				self.setRootNode( repo["key"], repo["name"] )
		
	def on_btnSelect_released(self, *args, **kwargs):
		if not self.multiple:
			for item in self.ui.listWidget.selectedItems():
				if isinstance( item, self.treeItem ):
					self.setSelection( [item.data] )
					event.emit( QtCore.SIGNAL("popWidget(PyQt_PyObject)"), self )
					return
			return
		else:
			self.setSelection( self.selected.get() )
		event.emit( QtCore.SIGNAL("popWidget(PyQt_PyObject)"), self )
	
	def on_listWidget_itemDoubleClicked(self, item):
		if isinstance( item, self.tree.treeItem ):
			if not self.multiple:
				self.setSelection( [item.data] )
				event.emit( QtCore.SIGNAL("popWidget(PyQt_PyObject)"), self )
				return
			else:
				if item.data in self.selected.get():
					return
				self.selected.extend( [item.data] )

	
	def on_btnAddSelected_released(self, *args, **kwargs ):
		items = self.tree.selectedItems()
		for item in items:
			if isinstance( item, self.treeItem ):
				if item.data in self.selected.get():
					continue
				self.selected.extend( [item.data] )

	def onDeleteCurrentSelection( self ):
		items = self.ui.listSelected.selectedItems()
		for item in items:
			self.ui.listSelected.takeItem( self.ui.listSelected.indexFromItem( item ).row() )
			self.selection.remove( item.data )




class TreeItemHandler( QtCore.QObject ):
	def __init__(self, *args, **kwargs ):
		QtCore.QObject.__init__( self, *args, **kwargs )
		self.connect( event, QtCore.SIGNAL('requestTreeItemViewDelegate(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), self.onRequestBoneViewDelegate ) #RegisterObj, ModulName, BoneName, SkelStructure
		self.connect( event, QtCore.SIGNAL('requestBoneEditWidget(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), self.onRequestBoneEditWidget ) 
		self.connect( event, QtCore.SIGNAL('requestTreeItemBoneSelection(PyQt_PyObject,PyQt_PyObject,PyQt_PyObject,PyQt_PyObject,PyQt_PyObject,PyQt_PyObject)'), self.RelationalBoneSeletor )
	
	def onRequestBoneViewDelegate(self, registerObject, modulName, boneName, skelStructure):
		if skelStructure[boneName]["type"].startswith("treeitem."):
			registerObject.registerHandler( 10, lambda: TreeItemViewBoneDelegate() )

	def onRequestBoneEditWidget(self, registerObject,  modulName, boneName, skelStructure ):
		if skelStructure[boneName]["type"].startswith("treeitem."):
			registerObject.registerHandler( 10, TreeItemEditBone( modulName, boneName, skelStructure ) )

	def RelationalBoneSeletor(self, registerObject, modulName, boneName, skelStructure, selection, setSelection ):
		if skelStructure[boneName]["type"].startswith("treeitem."):
			registerObject.registerHandler( 10, lambda: BaseTreeItemBoneSelector( modulName, boneName, skelStructure, selection, setSelection ) )

_TreeItemHandler = TreeItemHandler()
