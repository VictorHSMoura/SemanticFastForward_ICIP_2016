# coding=utf8

from Tkinter import *
import Tkinter as tk
import Tkconstants, tkFileDialog
import os, matlab.engine, subprocess
from functools import partial
from video import Video
from hyperlapse import SemanticHyperlapse, InputError
import threading, sys

def AddLog(logText, text, textType):
	logText.configure(state='normal')
	logText.insert("end", text, textType)
	logText.configure(state='disabled')
	logText.update_idletasks()

def CreateLogWindow():
	log = tk.Toplevel(root)
	text = tk.Text(log, wrap=WORD)
	scroll = tk.Scrollbar(root, command=text.yview)
	text.configure(yscrollcommand=scroll.set)
	text.tag_configure('italics', font=('Arial', 10, 'italic'))
	text.tag_configure('title', font=('Arial', 12, 'bold'))
	text.tag_configure('normal', font=('Arial', 10))
	text.pack()
	text.update_idletasks()
	log.title("Semantic Hyperlapse Status")
	return text

def PreProcessAndRun(hyperlapse, inputSpeedUp, alphaInput, betaInput, gamaInput, etaInput, errorLabel):
	speed = inputSpeedUp.get()
	try:
		alpha = [a.get() for a in alphaInput]
		beta = [b.get() for b in betaInput]
		gama = [g.get() for g in gamaInput]
		eta = [e.get() for e in etaInput]

		hyperlapse.setup(speed, alpha, beta, gama, eta)
		text = CreateLogWindow()
		hyperlapse.run([AddLog, text])
	except InputError as IE:
		errorLabel['text'] = IE.msg
		errorLabel.grid(row=7, columnspan=3)

def OpenFile(label, inputFileName, hyperlapse):
	hyperlapse.video.setVideoFile(tkFileDialog.askopenfilename(filetypes=([('All files', '*.*'), ('MP4 files', '*.mp4'), ('AVI files', '*.avi')])))
	hyperlapse.setPaths()

	inputFileName.set(hyperlapse.video.getVideoName())

def About():
	global root
	aboutscreen = tk.Toplevel(root)
	text = tk.Text(aboutscreen, wrap=WORD)
	scroll = tk.Scrollbar(root, command=text.yview)
	text.configure(yscrollcommand=scroll.set)
	text.tag_configure('italics', font=('Arial', 10, 'italic'))
	text.tag_configure('title', font=('Arial', 15, 'bold'))
	text.tag_configure('normal', font=('Arial', 10))
	text.insert(tk.END, "About\n\n", 'title')
	text.insert(tk.END, "See more about the project on:\n", 'normal')
	text.insert(tk.END, "\thttps://github.com/verlab/SemanticFastForward_ICIP_2016\n", 'italics')
	text.configure(state='disabled')
	text.pack()
	aboutscreen.title("About")

def Help():
	helpscreen = tk.Toplevel(root)
	text = tk.Text(helpscreen, wrap=WORD)
	scroll = tk.Scrollbar(root, command=text.yview)
	text.configure(yscrollcommand=scroll.set)
	text.tag_configure('bold_italics', font=('Arial', 10, 'bold', 'italic'))
	text.tag_configure('title', font=('Arial', 15, 'bold'))
	text.tag_configure('normal', font=('Arial', 10))
	text.insert(tk.END, "Instructions:\n\n", 'title')
	text.insert(tk.END, "1: ", 'bold_italics')
	text.insert(tk.END, "Go to File->OpenFile and select the video file that will be accelerated.\n", 'normal')
	text.insert(tk.END, "2: ", 'bold_italics')
	text.insert(tk.END, "Choose the speedup (speedup > 1).\n", 'normal')
	text.insert(tk.END, "3: ", 'bold_italics')
	text.insert(tk.END, "Choose graph weights α, β, γ, η. If you don't change anything, the default parameters will be used.\n", 'normal')
	text.insert(tk.END, "4: ", 'bold_italics')
	text.insert(tk.END, "Click on \"Speed Up Video\" and see the progress while your video is being accelerated.\n", 'normal')
	text.configure(state='disabled')
	text.pack()
	helpscreen.title("Help")

def startMenu():
	global root
	
	inputFileLabel = Label(root, text = "Input File: ").grid(row=0, sticky=W)
	inputFileName = StringVar()
	inputFile = Label(root, textvariable = inputFileName)

	speedUpLabel = Label(root, text = "Final Speed: ").grid(row=1, sticky=W)
	inputSpeedUp = tk.Entry(root, width=4)
		
	alphaLabel = Label(root, text = "α Weights: ").grid(row=2, sticky=W)
	alphaInput = [tk.Entry(root, width=4) for _ in range(2)]
	[alpha.insert(0, '50') for alpha in alphaInput]
	
	betaLabel = Label(root, text = "β Weights: ").grid(row=3, sticky=W)
	betaInput = [tk.Entry(root, width=4) for _ in range(2)]
	[beta.insert(0, '50') for beta in betaInput]
	
	gamaLabel = Label(root, text = "γ Weights: ").grid(row=4, sticky=W)
	gamaInput = [tk.Entry(root, width=4) for _ in range(2)]
	[gama.insert(0, '50') for gama in gamaInput]
	
	etaLabel = Label(root, text = "η Weights: ").grid(row=5, sticky=W)
	etaInput = [tk.Entry(root, width=4) for _ in range(2)]
	[eta.insert(0, '50') for eta in etaInput]

	errorLabel = Label(root, text = "")

	speedUpButton = Button(root, text="Speed Up Video", command=partial(PreProcessAndRun, hyperlapse, inputSpeedUp, alphaInput, betaInput, gamaInput, etaInput, errorLabel)).grid(row=6, column=1)

	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="OpenFile", command=partial(OpenFile, inputFile, inputFileName, hyperlapse))
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help Index", command=Help)
	helpmenu.add_command(label="About...", command=About)
	menubar.add_cascade(label="Help", menu=helpmenu)

	root.config(menu=menubar)
	root.title("Semantic Hyperlapse")

	inputFile.grid(row=0, column=1, columnspan=2)
	inputSpeedUp.grid(row=1, column=1, columnspan=2, sticky=W+E+N+S)
	[alphaInput[i].grid(row=2, column=i+1) for i in range(len(alphaInput))]
	[betaInput[i].grid(row=3, column=i+1) for i in range(len(betaInput))]
	[gamaInput[i].grid(row=4, column=i+1) for i in range(len(gamaInput))]
	[etaInput[i].grid(row=5, column=i+1) for i in range(len(etaInput))]

video = Video()
hyperlapse = SemanticHyperlapse()
hyperlapse.setVideo(video)

root = Tk()
startMenu()
root.mainloop()
