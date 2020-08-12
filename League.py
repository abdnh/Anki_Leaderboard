from PyQt5 import QtCore, QtGui, QtWidgets
import requests

from aqt import mw
from aqt.qt import *
from aqt.utils import showWarning, showInfo

def load_league(self):
	### GET DATA ###

	config = mw.addonManager.getConfig(__name__)
	url = 'https://ankileaderboard.pythonanywhere.com/league/'
	try:
		data = requests.get(url, timeout=20).json()
	except:
		showWarning("Timeout error - No internet connection, or server response took too long.")

	for i in data:
		if config["username"] in i:
			user_league_name = i[5]

	self.dialog.league_label.setText(user_league_name)

	### BUILD TABLE ###

	counter = 0
	for i in data:
		username = i[0]
		xp = i[1]
		reviews = i[2]
		time_spend = i[3]
		retention = i[4]
		league_name = i[5]

		if league_name == user_league_name:
			counter += 1

			rowPosition = self.dialog.League.rowCount()
			self.dialog.League.setColumnCount(5)
			self.dialog.League.insertRow(rowPosition)

			self.dialog.League.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))
			self.dialog.League.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(str(xp)))
			self.dialog.League.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(str(reviews)))
			self.dialog.League.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(str(time_spend)))
			self.dialog.League.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(str(retention)))

			#self.dialog.League.resizeColumnsToContents()

			if username in config['friends']:
				for j in range(self.dialog.League.columnCount()):
					self.dialog.League.item(counter-1, j).setBackground(QtGui.QColor("#2176ff"))
			if username == config['username']:
				for j in range(self.dialog.League.columnCount()):
					self.dialog.League.item(counter-1, j).setBackground(QtGui.QColor("#51f564"))

	### SCROLL ###

	current_ranking_list = []
	if config["scroll"] == True:
		for i in range(self.dialog.League.rowCount()):
			item = self.dialog.League.item(i, 0).text()
			current_ranking_list.append(item)
			if item == config['username']:
				userposition = self.dialog.League.item(current_ranking_list.index(item), 0)
				self.dialog.League.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)
				self.dialog.League.selectRow(current_ranking_list.index(item))
				self.dialog.League.clearSelection()
	
	### HIGHLIGHT ###

	users = self.dialog.League.rowCount()

	if user_league_name == "Delta":
		threshold = int((users / 100) * 20)
	if user_league_name == "Gamma":
		threshold = int((users / 100) * 15)
	if user_league_name == "Beta":
		threshold = int((users / 100) * 10)
	if user_league_name == "Alpha":
		threshold = int((users / 100) * 10)

	for i in range(threshold):
		for j in range(self.dialog.League.columnCount()):
			item = self.dialog.League.item(i, 0).text()
			if item == config['username']:
				continue
			else:
				self.dialog.League.item(i, j).setBackground(QtGui.QColor("#abffc7"))

	for j in range(self.dialog.League.columnCount()):
		self.dialog.League.item(0, j).setBackground(QtGui.QColor("#ffd700"))
		self.dialog.League.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
		self.dialog.League.item(2, j).setBackground(QtGui.QColor("#bf8970"))

	for i in range((users - threshold), users):
		for j in range(self.dialog.League.columnCount()):
			item = self.dialog.League.item(i, 0).text()
			if item == config['username']:
				self.dialog.League.item(i, j).setBackground(QtGui.QColor("#f21818"))
			else:
				self.dialog.League.item(i, j).setBackground(QtGui.QColor("#f75e5e"))  

