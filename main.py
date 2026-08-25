import tkinter as tk
from tkinter import ttk, messagebox
from app.agent import SupportAgent

BG='#0B1020'; PANEL='#11182A'; PANEL2='#151E33'; BORDER='#25314D'
TEXT='#F4F7FB'; MUTED='#8D9AB5'; ACCENT='#5EE7D2'; BLUE='#7C8CFF'
SUCCESS='#46D369'; WARNING='#F4C95D'; DANGER='#FF6B7A'

class AsterRowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Aster & Row | AI Customer Support Desk')
        self.geometry('1280x800'); self.minsize(1050,680); self.configure(bg=BG)
        self.agent=SupportAgent(); self._styles(); self._ui(); self._welcome()
        self.bind('<Control-Return>', lambda e: self.send_message())
        self.bind('<Escape>', lambda e: self.clear_input())

    def _styles(self):
        s=ttk.Style(self); s.theme_use('clam')
        s.configure('Accent.TButton',background=ACCENT,foreground='#071019',borderwidth=0,padding=(18,10),font=('Segoe UI Semibold',10))
        s.map('Accent.TButton',background=[('active','#7AF1E1')])
        s.configure('Ghost.TButton',background=PANEL2,foreground=TEXT,borderwidth=1,bordercolor=BORDER,padding=(12,8),font=('Segoe UI',9))
        s.map('Ghost.TButton',background=[('active','#202B45')])

    def _ui(self):
        self.grid_rowconfigure(0,weight=1); self.grid_columnconfigure(1,weight=1)
        self._sidebar(); self._main()

    def _sidebar(self):
        side=tk.Frame(self,bg=PANEL,width=275,highlightthickness=1,highlightbackground=BORDER)
        side.grid(row=0,column=0,sticky='nsew'); side.grid_propagate(False)
        brand=tk.Frame(side,bg=PANEL); brand.pack(fill='x',padx=22,pady=(25,18))
        c=tk.Canvas(brand,width=42,height=42,bg=PANEL,highlightthickness=0); c.pack(side='left')
        c.create_oval(4,4,38,38,fill=ACCENT,outline=''); c.create_text(21,21,text='A',fill='#071019',font=('Segoe UI Semibold',18))
        b=tk.Frame(brand,bg=PANEL); b.pack(side='left',padx=(10,0))
        tk.Label(b,text='ASTER & ROW',bg=PANEL,fg=TEXT,font=('Segoe UI Semibold',13)).pack(anchor='w')
        tk.Label(b,text='AI SUPPORT DESK',bg=PANEL,fg=ACCENT,font=('Segoe UI',8)).pack(anchor='w',pady=(2,0))
        ttk.Button(side,text='+  New conversation',style='Accent.TButton',command=self.new_conversation).pack(fill='x',padx=20,pady=(2,22))
        tk.Label(side,text='WORKSPACE',bg=PANEL,fg=MUTED,font=('Segoe UI Semibold',8)).pack(anchor='w',padx=22,pady=(0,8))
        self._nav(side,'Chat',True); self._nav(side,'Order lookup',False); self._nav(side,'Knowledge base',False)
        tk.Label(side,text='QUICK QUESTIONS',bg=PANEL,fg=MUTED,font=('Segoe UI Semibold',8)).pack(anchor='w',padx=22,pady=(28,8))
        for q in ['What is the return window?','Where is my order ORD-1007?','Do you ship to Canada?','What is the warranty?']:
            tk.Button(side,text=q,command=lambda x=q:self.use_prompt(x),bg=PANEL,fg=MUTED,activebackground=PANEL2,activeforeground=TEXT,relief='flat',anchor='w',cursor='hand2',font=('Segoe UI',9),padx=22,pady=6,borderwidth=0).pack(fill='x')
        status=tk.Frame(side,bg=PANEL2,highlightthickness=1,highlightbackground=BORDER); status.pack(side='bottom',fill='x',padx=16,pady=18)
        tk.Label(status,text='SYSTEM STATUS',bg=PANEL2,fg=MUTED,font=('Segoe UI Semibold',8)).pack(anchor='w',padx=14,pady=(12,8))
        for a,v in [('Agent','ONLINE'),('Knowledge base','READY'),('Order data','CONNECTED'),('Memory','ENABLED')]: self._status(status,a,v)
        tk.Label(status,text='Local deterministic demo',bg=PANEL2,fg=MUTED,font=('Segoe UI',7)).pack(anchor='w',padx=14,pady=(8,12))

    def _nav(self,p,text,active):
        bg='#1C2842' if active else PANEL; f=tk.Frame(p,bg=bg); f.pack(fill='x',padx=12,pady=2)
        tk.Label(f,text='●',bg=bg,fg=ACCENT if active else BORDER,font=('Segoe UI',8)).pack(side='left',padx=(10,8),pady=8)
        tk.Label(f,text=text,bg=bg,fg=TEXT if active else MUTED,font=('Segoe UI Semibold' if active else 'Segoe UI',9)).pack(side='left',pady=8)

    def _status(self,p,label,value):
        r=tk.Frame(p,bg=PANEL2); r.pack(fill='x',padx=14,pady=2)
        tk.Label(r,text='●',bg=PANEL2,fg=SUCCESS,font=('Segoe UI',8)).pack(side='left')
        tk.Label(r,text=label,bg=PANEL2,fg=TEXT,font=('Segoe UI',8)).pack(side='left',padx=(6,0))
        tk.Label(r,text=value,bg=PANEL2,fg=SUCCESS,font=('Segoe UI Semibold',7)).pack(side='right')

    def _main(self):
        main=tk.Frame(self,bg=BG); main.grid(row=0,column=1,sticky='nsew'); main.grid_rowconfigure(1,weight=1); main.grid_columnconfigure(0,weight=1)
        h=tk.Frame(main,bg=BG,height=92); h.grid(row=0,column=0,sticky='ew'); h.grid_propagate(False)
        l=tk.Frame(h,bg=BG); l.pack(side='left',padx=28,pady=20)
        tk.Label(l,text='Customer Support',bg=BG,fg=TEXT,font=('Segoe UI Semibold',19)).pack(anchor='w')
        tk.Label(l,text='Aster & Row AI assistant  •  grounded in company policies and safe order data',bg=BG,fg=MUTED,font=('Segoe UI',9)).pack(anchor='w',pady=(3,0))
        self.handoff=tk.Label(h,text='●  HUMAN HANDOFF: READY',bg='#10251E',fg=SUCCESS,padx=12,pady=7,font=('Segoe UI Semibold',8)); self.handoff.pack(side='right',padx=28,pady=24)
        box=tk.Frame(main,bg='#0D1425',highlightthickness=1,highlightbackground=BORDER); box.grid(row=1,column=0,sticky='nsew',padx=22,pady=(0,12)); box.grid_rowconfigure(0,weight=1); box.grid_columnconfigure(0,weight=1)
        self.canvas=tk.Canvas(box,bg='#0D1425',highlightthickness=0); self.canvas.grid(row=0,column=0,sticky='nsew')
        sb=ttk.Scrollbar(box,orient='vertical',command=self.canvas.yview); sb.grid(row=0,column=1,sticky='ns'); self.canvas.configure(yscrollcommand=sb.set)
        self.chat=tk.Frame(self.canvas,bg='#0D1425'); self.window=self.canvas.create_window((0,0),window=self.chat,anchor='nw')
        self.chat.bind('<Configure>',lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all'))); self.canvas.bind('<Configure>',lambda e:self.canvas.itemconfigure(self.window,width=e.width))
        comp=tk.Frame(main,bg=BG); comp.grid(row=2,column=0,sticky='ew',padx=22,pady=(0,18))
        inp=tk.Frame(comp,bg=PANEL,highlightthickness=1,highlightbackground=BORDER); inp.pack(fill='x')
        self.input=tk.Text(inp,height=3,wrap='word',bg=PANEL,fg=TEXT,insertbackground=ACCENT,selectbackground='#2C3C63',relief='flat',font=('Segoe UI',10),padx=14,pady=12)
        self.input.pack(side='left',fill='both',expand=True,padx=(4,0),pady=4); self.input.bind('<Return>',self._enter)
        a=tk.Frame(inp,bg=PANEL); a.pack(side='right',padx=10,pady=8)
        ttk.Button(a,text='Clear',style='Ghost.TButton',command=self.clear_input).pack(pady=(0,8)); ttk.Button(a,text='Send  Ctrl+Enter',style='Accent.TButton',command=self.send_message).pack()
        tk.Label(comp,text='AI answers are grounded in the provided knowledge base and customer-safe order data.',bg=BG,fg=MUTED,font=('Segoe UI',7)).pack(anchor='w',pady=(7,0))

    def _welcome(self):
        self._msg('assistant','Welcome to Aster & Row Support.','I can help with returns, shipping, warranty questions, and customer-safe order status.')
        self._msg('assistant','Try a question like:','• What is the return window?\n• Where is order ORD-1007?\n• Does Aster & Row ship to Canada?\n• What is the warranty period?')

    def _msg(self,role,title,body,sources=None,handoff=False):
        row=tk.Frame(self.chat,bg='#0D1425'); row.pack(fill='x',padx=20,pady=10)
        user=role=='user'; bg='#243152' if user else '#18243A'; accent=BLUE if user else ACCENT; anchor='e' if user else 'w'
        wrap=tk.Frame(row,bg='#0D1425'); wrap.pack(anchor=anchor)
        tk.Label(wrap,text='YOU' if user else 'A&R',bg=accent,fg='#071019',font=('Segoe UI Semibold',7),padx=8,pady=5).pack(anchor=anchor,pady=(0,4))
        bubble=tk.Frame(wrap,bg=bg,highlightthickness=1,highlightbackground=BORDER); bubble.pack()
        tk.Label(bubble,text=title,bg=bg,fg=TEXT,font=('Segoe UI Semibold',10),justify='left',anchor='w').pack(fill='x',padx=14,pady=(11,3))
        tk.Label(bubble,text=body,bg=bg,fg='#D6DEEE',font=('Segoe UI',9),justify='left',anchor='w',wraplength=720).pack(fill='x',padx=14,pady=(0,11))
        if sources:
            tk.Label(bubble,text='SOURCE  '+'   •   '.join(sources),bg=bg,fg=ACCENT,font=('Segoe UI Semibold',7),justify='left',anchor='w',wraplength=720).pack(fill='x',padx=14,pady=(0,8))
        if handoff:
            tk.Label(bubble,text='HUMAN REVIEW RECOMMENDED',bg='#34291A',fg=WARNING,font=('Segoe UI Semibold',7),padx=8,pady=5).pack(anchor='w',padx=14,pady=(0,11))
        self.after(20,lambda:self.canvas.yview_moveto(1.0))

    def _enter(self,event):
        if event.state & 4: self.send_message(); return 'break'

    def send_message(self):
        msg=self.input.get('1.0','end').strip()
        if not msg:return
        self.input.delete('1.0','end'); self._msg('user','You',msg); self.configure(cursor='watch'); self.update_idletasks()
        try:
            r=self.agent.respond(msg); self._msg('assistant','Aster & Row Assistant',r.get('answer','No answer returned.'),r.get('sources',[]),r.get('handoff',False))
            if r.get('handoff'):
                self.handoff.configure(text='●  HUMAN HANDOFF: RECOMMENDED',bg='#34291A',fg=WARNING)
            else:
                self.handoff.configure(text='●  HUMAN HANDOFF: READY',bg='#10251E',fg=SUCCESS)
        except Exception as exc:
            self._msg('assistant','Something went wrong',f'The support agent could not complete this request.\nError: {exc}',handoff=True)
            self.handoff.configure(text='●  HUMAN HANDOFF: ERROR',bg='#351B24',fg=DANGER)
        finally:self.configure(cursor=''); self.input.focus_set()

    def use_prompt(self,prompt): self.input.delete('1.0','end'); self.input.insert('1.0',prompt); self.input.focus_set()
    def clear_input(self): self.input.delete('1.0','end'); self.input.focus_set()

    def new_conversation(self):
        if not messagebox.askyesno('New conversation','Start a new support conversation?'): return
        self.agent=SupportAgent()
        for w in self.chat.winfo_children(): w.destroy()
        self.handoff.configure(text='●  HUMAN HANDOFF: READY',bg='#10251E',fg=SUCCESS); self._welcome(); self.input.focus_set()

if __name__=='__main__': AsterRowApp().mainloop()