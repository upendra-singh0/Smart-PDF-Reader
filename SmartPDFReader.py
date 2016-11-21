import sys
import urllib2

from PyQt4 import QtGui
from cStringIO import StringIO

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from wordnik import swagger
from wordnik.WordApi import WordApi
from wordnik.WordsApi import WordsApi

apiUrl = 'http://api.wordnik.com/v4'
apiKey = '524d83a00b161d350b0000e507e0a74bc987f39ec4da39222'
client = swagger.ApiClient(apiKey, apiUrl)

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)

        self.filename = ""

        self.initUI()

    def initToolbar(self):
        #menu

        self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        self.openAction.setStatusTip("Open existing document")
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)


        self.printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
        self.printAction.setStatusTip("Print document")
        self.printAction.setShortcut("Ctrl+P")
        self.printAction.triggered.connect(self.printHandler)

        self.previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"),"Page view",self)
        self.previewAction.setStatusTip("Preview page before printing")
        self.previewAction.setShortcut("Ctrl+Shift+P")
        self.previewAction.triggered.connect(self.preview)


        self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.searchAction = QtGui.QAction(QtGui.QIcon("icons/find.png"), "search in dictionary", self)
        self.searchAction.setStatusTip("Search in dictionary")
        self.searchAction.setShortcut("Ctrl+D")
        self.searchAction.triggered.connect(self.search)

        self.wordAction = QtGui.QAction(QtGui.QIcon("icons/font-size.png"), "Word of the day", self)
        self.wordAction.setStatusTip("Word of the day")
        self.wordAction.setShortcut("Ctrl+W")
        self.wordAction.triggered.connect(self.word)

        self.allExamples = QtGui.QAction(QtGui.QIcon("icons/bullet.png"), "Examples", self)
        self.allExamples .setStatusTip("Examples")
        self.allExamples .setShortcut("Ctrl+E")
        self.allExamples .triggered.connect(self.getexamples)

        self.topExample = QtGui.QAction(QtGui.QIcon("icons/indent.png"), "Top example", self)
        self.topExample.setStatusTip("Top example")
        self.topExample.setShortcut("Ctrl+M")
        self.topExample.triggered.connect(self.gettopexample)

        self.relatedwords = QtGui.QAction(QtGui.QIcon("icons/count.png"), "Related words", self)
        self.relatedwords.setStatusTip("Related words")
        self.relatedwords.setShortcut("Ctrl+R")
        self.relatedwords.triggered.connect(self.getrelatedwords)



        self.toolbar = self.addToolBar("Options")
        self.toolbar.addAction(self.openAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        self.toolbar.addSeparator()

        self.toolbar.addAction(self.copyAction)
        self.toolbar.addSeparator()

        self.toolbar.addAction(self.searchAction)
        self.toolbar.addAction(self.wordAction)
        self.toolbar.addAction(self.allExamples)
        self.toolbar.addAction(self.topExample)
        self.toolbar.addAction(self.relatedwords)



        self.toolbar.addSeparator()

        # Makes the next toolbar appear underneath this one
        self.addToolBarBreak()

    def initMenubar(self):

      menubar = self.menuBar()

      file = menubar.addMenu("File")
      edit = menubar.addMenu("Edit")
      view = menubar.addMenu("View")

      file.addAction(self.openAction)
      file.addAction(self.printAction)
      file.addAction(self.previewAction)

      edit.addAction(self.copyAction)
      view.addAction(self.searchAction)
      view.addAction(self.wordAction)
      view.addAction(self.allExamples)
      view.addAction(self.topExample)
      view.addAction(self.relatedwords)


    def initUI(self):

        self.text = QtGui.QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setText("Simple PDF Reader")


        self.initToolbar()
        self.initMenubar()

        # Set the tab stop width to around 33 pixels which is
        # about 8 spaces
        self.text.setTabStopWidth(33)

        self.setCentralWidget(self.text)

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # If the cursor position changes, call the function that displays
        # the line and column number
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1030,800)

        self.setWindowTitle("PDF Reader")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))
    def new(self):

        spawn = Main(self)
        spawn.show()

    def open(self):

        # Get filename and show only .writer files
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","(*.pdf)")
        print 'open file'
        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(convert(self.filename))

    def save(self):

        # Only open dialog if there is no filename yet
        if not self.filename:
          self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

        # Append extension if not there yet
        if not self.filename.endswith(".writer"):
          self.filename += ".writer"

        # We just store the contents of the text file along with the
        # format in html, which Qt does in a very nice way for us
        with open(self.filename,"wt") as file:
            file.write(self.text.toHtml())

    def preview(self):

        # Open preview dialog
        preview = QtGui.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))
        preview.exec_()

    def printHandler(self):

        # Open printing dialog
        dialog = QtGui.QPrintDialog()

        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def cursorPosition(self):
        cursor = self.text.textCursor()

        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line, col))



    def search(self):
        print 'check search functiom def'
        cursor = self.text.textCursor()
        print cursor.hasSelection()

        isConnected = 1
        req = urllib2.Request('http://www.google.com')
        try: urllib2.urlopen(req)
        except urllib2.URLError as e:
            print(e.reason)
            isConnected = 0

        if(isConnected == 0):
            print 'Please connect to Internet'
            self.statusbar.showMessage("Please connect to Internet.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please connect to Internet.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


        elif (cursor.hasSelection and QString(cursor.selectedText()).trimmed().length()>=1 and isConnected):
            textSelected = cursor.selectedText()
            qString = QString(textSelected)
            d = QDialog(self)
            d.setGeometry(300,200,263,195)
            d.setWindowTitle(textSelected)

            wordApi = WordApi(client)
            example = wordApi.getDefinitions(qString.toLower())

            if example is not None:
                print 'not none'

                d.textedit = QtGui.QTextEdit(d)
                d.textedit.setPlainText(textSelected)
                d.textedit.setReadOnly(True)
                d.textedit.setAutoFillBackground(True)
                for index in xrange(len(example)):
                    if example[index].partOfSpeech == 'noun':
                        d.textedit.append('n. '+ example[index].text)
                    elif example[index].partOfSpeech == 'verb-transitive':
                        d.textedit.append('transitive v. '+ example[index].text)
                    elif example[index].partOfSpeech == 'phrasal-verb':
                        d.textedit.append('phrasal v. ' + example[index].text)
                    elif example[index].partOfSpeech == 'idiom':
                        d.textedit.append('idiom. ' + example[index].text)
                    elif example[index].partOfSpeech == 'adjective':
                        d.textedit.append('adj. ' + example[index].text)
                    else:
                        d.textedit.append(example[index].text)
                d.exec_()

            else:
                print 'Cannot be found'
                self.statusbar.showMessage("Please select a word or letter.")
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setInformativeText("Sorry no defination found.")
                msg.setWindowTitle(textSelected)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

        else:
            print 'no text selected'
            self.statusbar.showMessage("Please select a word or letter.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText("Please select a word or a letter.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok )
            msg.exec_()

    def showdialog(self):
         msg = QMessageBox()
         msg.setIcon(QMessageBox.Information)
         msg.setText("This is a message box")
         msg.setInformativeText("This is additional information")
         msg.setWindowTitle("MessageBox demo")
         msg.setDetailedText("The details are as follows:")
         msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
         msg.exec_()

    def word(self):
        isConnected = 1
        req = urllib2.Request('http://www.google.com')
        try:
            urllib2.urlopen(req)
        except urllib2.URLError as e:
            print(e.reason)
            isConnected = 0

        if (isConnected == 0):
            print 'Please connect to Internet'
            self.statusbar.showMessage("Please connect to Internet.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please connect to Internet.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        elif (isConnected):

            wordApi = WordsApi(client)
            dayword = wordApi.getWordOfTheDay();

            if dayword is not None:
                d = QDialog(self)
                d.setGeometry(300, 200, 263, 195)
                d.setWindowTitle(dayword.word)
                print dayword.word

                d.textedit = QtGui.QTextEdit(d)
                d.textedit.setPlainText(dayword.word)
                d.textedit.setReadOnly(True)
                d.textedit.setAutoFillBackground(True)
                for index in xrange(len(dayword.examples)):
                        d.textedit.append(str(index+1) + ". "+ dayword.examples[index].text)
                d.exec_()
            else:
                self.statusbar.showMessage("Please try after some time.")
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setInformativeText("Please try after some time.")
                msg.setWindowTitle("Alert")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def getexamples(self):
        cursor = self.text.textCursor()
        print cursor.hasSelection()

        isConnected = 1
        req = urllib2.Request('http://www.google.com')
        try:
            urllib2.urlopen(req)
        except urllib2.URLError as e:
            print(e.reason)
            isConnected = 0

        if (isConnected == 0):
            print 'Please connect to Internet'
            self.statusbar.showMessage("Please connect to Internet.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please connect to Internet.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


        elif (cursor.hasSelection and QString(cursor.selectedText()).trimmed().length() >= 1 and isConnected):
            textSelected = cursor.selectedText()
            qString = QString(textSelected)
            d = QDialog(self)
            d.setGeometry(300, 200, 263, 195)
            d.setWindowTitle(textSelected)

            wordApi = WordApi(client)
            example = wordApi.getExamples(qString.toLower())

            if example is not None:
                print 'not none'

                d.textedit = QtGui.QTextEdit(d)
                d.textedit.setPlainText("Examples: "+ textSelected)
                d.textedit.setReadOnly(True)
                d.textedit.setAutoFillBackground(True)
                for index in xrange(len(example.examples)):
                        d.textedit.append(str(index+1) + ". "+example.examples[index].text)
                d.exec_()

            else:
                print 'Cannot be found'
                self.statusbar.showMessage("Sorry no defination found.")
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setInformativeText("Sorry no defination found.")
                msg.setWindowTitle(textSelected)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

        else:
            print 'no text selected'
            self.statusbar.showMessage("Please select a word or letter.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText("Please select a word or a letter.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def gettopexample(self):
        cursor = self.text.textCursor()
        print cursor.hasSelection()

        isConnected = 1
        req = urllib2.Request('http://www.google.com')
        try:
            urllib2.urlopen(req)
        except urllib2.URLError as e:
            print(e.reason)
            isConnected = 0

        if (isConnected == 0):
            print 'Please connect to Internet'
            self.statusbar.showMessage("Please connect to Internet.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please connect to Internet.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


        elif (cursor.hasSelection and QString(cursor.selectedText()).trimmed().length() >= 1 and isConnected):
            textSelected = cursor.selectedText()
            qString = QString(textSelected)
            d = QDialog(self)
            d.setGeometry(300, 200, 263, 195)
            d.setWindowTitle(textSelected)

            wordApi = WordApi(client)
            example = wordApi.getTopExample(qString.toLower())

            if example is not None:
                print 'not none'

                d.textedit = QtGui.QTextEdit(d)
                d.textedit.setPlainText("Top Example: " + textSelected)
                d.textedit.setReadOnly(True)
                d.textedit.setAutoFillBackground(True)
                d.textedit.append(example.text)
                d.exec_()

            else:
                print 'Cannot be found'
                self.statusbar.showMessage("Sorry nothing found.")
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setInformativeText("Sorry nothing found.")
                msg.setWindowTitle(textSelected)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

        else:
            print 'no text selected'
            self.statusbar.showMessage("Please select a word or letter.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText("Please select a word or a letter.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def getrelatedwords(self):
        cursor = self.text.textCursor()
        print cursor.hasSelection()

        isConnected = 1
        req = urllib2.Request('http://www.google.com')
        try:
            urllib2.urlopen(req)
        except urllib2.URLError as e:
            print(e.reason)
            isConnected = 0

        if (isConnected == 0):
            print 'Please connect to Internet'
            self.statusbar.showMessage("Please connect to Internet.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Please connect to Internet.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


        elif (cursor.hasSelection and QString(cursor.selectedText()).trimmed().length() >= 1 and isConnected):
            textSelected = cursor.selectedText()
            qString = QString(textSelected)
            d = QDialog(self)
            d.setGeometry(300, 200, 263, 195)
            d.setWindowTitle(textSelected)

            wordApi = WordApi(client)
            example = wordApi.getRelatedWords(qString.toLower())

            if example is not None:

                d.textedit = QtGui.QTextEdit(d)
                d.textedit.setPlainText("Related words of " + textSelected)
                d.textedit.setReadOnly(True)
                d.textedit.setAutoFillBackground(True)
                for index in xrange(len(example)):
                    if example[index].relationshipType == 'verb-form':
                        d.textedit.setFontItalic(True)
                        d.textedit.append('verb-form:')
                        d.textedit.setFontItalic(False)
                        for i in xrange(len(example[index].words)):
                            d.textedit.append(str(i+1)+". " + example[index].words[i])
                    elif example[index].relationshipType == 'hypernym':
                        d.textedit.append('\n hypernym:')
                        for i in xrange(len(example[index].words)):
                            d.textedit.append(str(i+1) + ". " + example[index].words[i])
                    if example[index].relationshipType == 'cross-reference':
                        d.textedit.append('\n cross-reference:')
                        for i in xrange(len(example[index].words)):
                            d.textedit.append(str(i+1) + ". " + example[index].words[i])
                    if example[index].relationshipType == 'variant':
                        d.textedit.append('\n variant:')
                        for i in xrange(len(example[index].words)):
                            d.textedit.append(str(i+1) + ". " + example[index].words[i])
                    if example[index].relationshipType == 'synonym':
                        d.textedit.append('\n synonym:')
                        for i in xrange(len(example[index].words)):
                            d.textedit.append(str(i+1) + ". " + example[index].words[i])
                    if example[index].relationshipType == 'rhyme':
                        d.textedit.append('\n rhyme:')
                        for i in xrange(len(example[index].words)):
                            d.textedit.append(str(i+1) + ". " + example[index].words[i])
                    if example[index].relationshipType == 'unknown':
                        d.textedit.append('\n unknown')
                        for i in xrange(len(example[index].words)):
                            d.textedit.append(str(i+1) + ". " + example[index].words[i])
                    if example[index].relationshipType == 'same-context':
                        d.textedit.append('\n same-context')
                        for i in xrange(len(example[index].words)):
                            d.textedit.append(str(i+1) + ". " + example[index].words[i])
                d.exec_()

            else:
                self.statusbar.showMessage("Sorry nothing found.")
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Question)
                msg.setInformativeText("Sorry nithing found.")
                msg.setWindowTitle(textSelected)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

        else:
            print 'no text selected'
            self.statusbar.showMessage("Please select a word or letter.")
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText("Please select a word or a letter.")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


def main():

    app = QtGui.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
