from tkinter import * 
import os
import pickle
from tkinter import messagebox as msg

with open('store.pickle', 'rb') as f:
	items = list(pickle.load(f))

r = Tk()

r.title('Contacts Book')

fr = Frame(r,bg='white')


def add(x,y):
	if len(x.strip()) != 0 and len(y.strip()) != 0: 
		val = f" {x}  -- {y}"
		contls.insert(END, val)
		items.append(val)
		idx = contls.get(0, "end").index(val)
		contls.delete(idx)
		contls.insert(idx, f'{idx + 1}. ' + val)
		items.pop(idx)
		items.append(f'{idx + 1}. ' + val)

Label(r, text='Name').pack()
name = Entry(r)
name.pack()

Label(r, text='Number').pack()
num = Entry(r)
num.pack()

w = Scrollbar(r)
w.pack(fill=BOTH, side=RIGHT)

contls = Listbox(fr, width=50,font=('Helvetica', 16), bg='white',highlightthickness=0, borderwidth=0)
btn = Button(r, text='add', command=lambda:add(name.get(),num.get()), font=('Helvetica', 12))
btn.pack(pady=6)
contls.pack(side=LEFT, fill=BOTH)

contls.config(yscrollcommand=w.set)
w.config(command=contls.yview)

def removeitem(index):
	contls.delete(index)
	items.pop(index)

def editvar(i,t):
	contls.delete(i)
	contls.insert(i, t)

def edititem(index):
	text = contls.get(index)
	top = Toplevel(r)
	edit = Entry(top)
	edit.pack()
	Button(top, text='submit', command=lambda : editvar(index,edit.get())).pack()

def create_menu(index,e):
	rmenu = Menu(r, tearoff=0)
	rmenu.add_command(label='remove contact', command=lambda: removeitem(index))
	rmenu.add_command(label='edit contact', command=lambda: edititem(index))
	try:
		rmenu.tk_popup(e.x_root, e.y_root)
	except:
		rmenu.grab_release()

	

def selected(e):
	s = e.widget.curselection()
	if s:
		i = s[0]
		data = e.widget.get(i)
		create_menu(i,e)


r.bind('<Return>', lambda x:add(name.get(),name.get()))
contls.bind('<Button-3>', selected)

fr.pack(ipadx=30)


for i in items:
	contls.insert(END,i)

def warn():
	val = msg.askyesno('Delete?', 'Are you Sure you want to delete all contacts!')
	if val == True:
		print('hi')

		for i in contls.get(0,'end'):
			index = contls.get(0,"end").index(i)
			removeitem(index)

Button(r, text='remove all', command=warn, font=('Helvetica', 12)).pack(pady=8)

r.mainloop()

with open('store.pickle', 'wb') as f:
	pickle.dump(items,f)
