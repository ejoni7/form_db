from copy import copy
from tkinter import *
from tkinter import messagebox
import os
import sys

win=Tk()
win.geometry('700x500')
win.title('form builder')
# ======= globals ======
builtins=('exit','format','any','all','bin','eval','exec','format','globals','help','hex','id',
'input','len','license','locals','max','min','next','open','pow','print','quit','read','repr',
'round','sorted','sum')
path_=os.path.abspath(sys.argv[0])

if path_[-8:-3] !='ejmin':
    raise RuntimeError('this module should run from ...ejmin.py')


# ========== function ========
def check_initial_validate(fields,striped_list):
    if not len(fields) == len(set(fields)):
        messagebox.showerror('nameing error','please enter unique field names')
        return False
        
    for i in map(lambda x: x.split('|')[1],striped_list[1]):
        if not i in ('int','str'):
            messagebox.showerror('invalid type','imput should be int or str')
            return False
    
    if not  ent_table.get():
        messagebox.showerror('empty table name','table name must be filled!')
        return False
    
    for i in( mix_list :=striped_list[2]+striped_list[3]):
        if i in builtins:
            messagebox.showerror('nameing error',
            f' name "{i}" is builtin function \n please choose other name')
            return False
        if not len(mix_list)==len(set(mix_list)):
            messagebox.showerror('nameing error','please enter unique button names')
            return False
    return True

def get_ejmin_db():
    with open('./ejmin_db.py','r') as f:
        x=f.read()
    return x

def database_stracture(list_):
    table_name = ent_table.get()
    types=[]
    tables=[ i.split('|') for i in list_]
    creational_fields=''
    insert_fields=''
    questins=''

    for i in tables:
        if i[1] not in ('int','str'):
            return None
        else:
            if i[1]=='int':
                creational_fields+=f', {i[0]} INTEGER '
                types.append('int')

            elif i[1]=='str':
                creational_fields +=f', {i[0]} TEXT'
                types.append('str')
            insert_fields+=f', {i[0]}'
            questins+=', ?'

    create_input=insert_fields.split(',')
    create_input.pop(0)
    create_input=list(map(lambda x: x.replace(' ',''),create_input))
    insert_update=copy(create_input)

    for index,i in enumerate(create_input):
        if types[index]=='int':
            create_input[index]=f'int({i})'
        insert_update[index]=f' {i} = ? '
        
    insert_update=','.join(insert_update)
    create_input=','.join(create_input)
    new_db=''
    
    if(db_content :=get_ejmin_db()).find('import sqlite3') == -1:
        new_db='import sqlite3\nfrom tkinter import messagebox\n\n'
        new_db+='''con=sqlite3.connect("./mydatabase.db")
cur=con.cursor()

class Common:
    def __init__(self,name, types) -> None:
        self.name=name
        self.types=types

    def valid(self,list_) -> list:
        
        for index,i in enumerate(list_) :
            if self.types[index]=='int':
                if not i.isnumeric():
                    return None
            elif self.types[index]=='str':
                if not i.isalpha():
                    return None
        return self.types

    def read(self, query=None, elements=None):
        if query and elements:
            query=query.replace('*','%')
            query=query.replace('?','_')
            searched=[query for i in elements]
            elements=list(map(lambda x : x+' like ? or ',elements))
            search_fields=''.join(elements)
            search_fields=search_fields[:-4]
            cur.execute(f'SELECT * FROM {self.name} WHERE {search_fields}',searched)
        else:
            cur.execute(f'SELECT * FROM {self.name}')
        return cur.fetchall()
        
    def delete(self, pk):
        cur.execute(f'DELETE FROM {self.name} WHERE id = ?',(pk,))
        con.commit()

    def get_record(self,pk):
        cur.execute(f'SELECT * FROM {self.name} WHERE id = ?',(pk,))
        return cur.fetchone()
'''
    if db_content.find(f'========= {table_name} =========')== -1:
        new_db +=f'''
# ========= {table_name} =========
class {table_name.capitalize()}(Common):
    def __init__(self):
        super().__init__( '{table_name}', {types})
        cur.execute('CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY{creational_fields})')
        con.commit()

    def create(self{insert_fields}):
        if self.valid([{insert_fields[1:]}]):
            cur.execute(f'INSERT INTO {table_name} (id{insert_fields}) VALUES(NULL{questins})',({create_input}))
            con.commit()
        else:
            messagebox.showerror('invalid data','please inter correct data')

    def update(self, pk{insert_fields}):
        if self.valid([{insert_fields[1:]}]):
            cur.execute(f'UPDATE {table_name} SET {insert_update} WHERE id= ?', ({create_input} ,pk))
            con.commit()
        else:
            messagebox.showerror('invalid data','please inter correct data')
    '''
    else:
        messagebox.showerror('error','table name created before')
        raise NameError('the table with this name crated before')
    return new_db


def form_final_stracture(valid_list):
    _=get_form_height_and_design(valid_list)
    new_form=f'''from tkinter import *
from ejmin_db import *
    
root=Tk()
root.geometry('500x{_[0]}')
root.title('new form')
root.resizable(0,0)'''
    new_form+='\n\n# ========== functions ==========='
    if ents:=list(map(lambda x: x.split('|')[0],(*valid_list[1],))):
        new_form +='\ndef clear():'
        for i in ents:
            new_form+=f'\n   lbl_ent_{i}.delete(0,END)'
        new_form += f'\n   lbl_ent_{ents[0]}.focus_set()'

    for i in (*valid_list[2],*valid_list[3]) :
        if not i=='clear':
            new_form+=f'\n\ndef {i}():\n   pass'
    new_form +=_[1]
    return new_form

def write_new_modules(new_form,data_base):
    with open(path_,'w',encoding='utf-8')as f:
        for line in new_form.splitlines():
            f.write(line + '\n')
    
    with open('./ejmin_db.py','a',encoding='utf-8')as f:
        for line in data_base.splitlines():
            f.write(line + '\n')
    
    messagebox.showinfo('success','your table is ready \nand connected to database')
    
               
def get_form_height_and_design(valid_list):
    design_string=''
    answer_=answer.get()
    
    height=10
    for index,i in enumerate(valid_list):
        if (x:=len(i))>0:
            if index==0:
                design_string +='\n\n# ========== labels ==========='
                design_string +=f"\nLabel(root,font='arial 20 bold',text='{' '.join(i)}').place(x=10,y={height})"
                height +=70
                continue
            if index==1:
                design_string+='\n\n# ========== label-entries ==========='
                for item in i:
                    item=item.split('|')[0]
                    design_string +=f'''\nLabel(root,font='arial 20 bold',text='{item}').place(x=10,y={height})
lbl_ent_{item}=Entry(root,font='arial 20 bold')
lbl_ent_{item}.place(x=180,y={height})\n'''
                    height+=65
                continue
            if answer_==1 and index==2:
                design_string+='\n\n# ========== list-box ==========='
                design_string +=f'''\nlist_box=Listbox(root)
list_box.place(x=50,y={height},width=400,height=200)'''
                height+=220
                
            if index==2:
                design_string+='\n\n# ========== button-entries ==========='
                for item in i:
                    design_string +=f'''\nButton(root,font='arial 20 bold',text='{item}',command={item}).place(x=10,y={height},width=150)
btn_ent_{item}=Entry(root,font='arial 20 bold')
btn_ent_{item}.place(x=180,y={height}+10)\n'''
                    height +=70
                continue

            if index==3 :
                design_string+='\n\n# ========== buttons ==========='
                if x%3==0:
                    for num,item in enumerate(i):
                        design_string+=f'''\nButton(root,font='arial 20 bold',text='{item}'
,command={item}).place(
    x=20+({num}%3)*160,y={height}+int({num}/3)*80,width=150)\n'''
                    height +=int(x/3)*70
                elif x%2==0:
                    for num,item in enumerate(i):
                        design_string +=f'''\nButton(root,font='arial 20 bold',text='{item}'
,command={item}).place(x=40+({num}%2)*220,y={height}+int({num}/2)*80,width=200)\n'''
                    height +=int(x/2)*70
                elif x==1:
                    design_string +=f'''\nButton(root,font='arial 20 bold',text='{i[0]}'
,command={i[0]}).place(x=200,y={height},width=200)\n'''
                    height +=70
    height +=10
    design_string +='\n\n\nroot.mainloop()'
    return ((height,design_string))

def build():
    list_=[ i.get().split(',') for i in (entry_lbl,entry_lbl_ent,entry_btn_ent,entry_btn)]
    striped_list=[ [item.strip() for item in inner if item.strip() !='']for inner in list_ ]
    fields=list(map(lambda x: x.split('|')[0],striped_list[1]))
    if check_initial_validate(fields,striped_list):
        new_form=form_final_stracture(striped_list)
        db_aditional_text=database_stracture(striped_list[1])
        write_new_modules(new_form,db_aditional_text)
    
    
#  ====== for label========
label_lbl=Label(win,text='label by "," ',font='arial 20 bold')
label_lbl.place(x=10,y=10)
entry_lbl=Entry(win,font='arial 20 bold')
entry_lbl.place(x=340,y=10,width=350)

# ========= for label-entries =======
label_lbl_ent=Label(win,text='label-entries "x|int,x|str" ',font='arial 20 bold')
label_lbl_ent.place(x=10,y=80)
entry_lbl_ent=Entry(win,font='arial 20 bold')
entry_lbl_ent.place(x=340,y=80,width=350)

# ========= for button-entry =======
label_btn_ent=Label(win,text='button-entry by "," ',font='arial 20 bold')
label_btn_ent.place(x=10,y=150)
entry_btn_ent=Entry(win,font='arial 20 bold')
entry_btn_ent.place(x=340,y=150,width=350)

# ========= for button =======
label_btn=Label(win,text='single button by "," ',font='arial 20 bold')
label_btn.place(x=10,y=220)
entry_btn=Entry(win,font='arial 20 bold')
entry_btn.place(x=340,y=220,width=350)

# ========= database table name =======
Label(win,text='table name ',font='arial 20 bold').place(x=10,y=300)
ent_table=Entry(win,font='arial 20 bold')
ent_table.place(x=340,y=300,width=350)

# ========= for listbox ==========
frame=LabelFrame(win,text='has listbox?',font='arial 20 bold')
frame.place(x=10,y=380,width=200,height=100)
answer=IntVar(value=0)
Radiobutton(frame,text='yes',variable=answer,value=1,font='arial 20 bold').place(x=10,y=0)
Radiobutton(frame,text='no',variable=answer,value=0,font='arial 20 bold').place(x=100,y=0)

# ======= submit boton ========
Button(win,text='create',font='arial 20 bold',command=build).place(x=275,y=400,width=150)


win.mainloop()

