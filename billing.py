from tkinter import*
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import sqlite3
import time
import os
import tempfile
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System ||  DEVELOPED By ME")
        self.root.resizable(False, False)
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print=0

        #===TITLE====
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text=" Inventory Management System",image=self.icon_title,compound=LEFT, font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)


        #===btn_logout===
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #======clock======
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH-MM-SS",font=("times new roman",15,"bold"),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)


        #=======product frame=======


        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626",
                       fg="white").pack(side=TOP, fill=X)

        # =======PRODUCT SEARCH FRAME=========

        self.var_search = StringVar()

        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=400, height=90)

        lbl_search = Label(ProductFrame2, text="Search Product || By Name", font=("times new roman", 15, "bold"),
                           bg="white", fg="green").place(x=2, y=5)

        lbl_search = Label(ProductFrame2, text="Product Name", font=("times new roman", 15, "bold"), bg="white").place(
            x=2, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15),
                           bg="lightyellow").place(x=130, y=48, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Search",command=self.search, font=("goudy old style", 15),
                            bg="#2196f3", fg="white", cursor="hand2").place(x=285, y=46, width=100, height=25)

        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, font=("goudy old style", 15),
                              bg="#083531", fg="white", cursor="hand2").place(x=285, y=10, width=100, height=25)

        # =======PRODUCT DETAILS FRAME=========
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=400, height=375)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="PID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="QTY")
        self.product_table.heading("status", text="Status")
        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=40)
        self.product_table.column("name", width=90)
        self.product_table.column("price", width=100)
        self.product_table.column("qty", width=40)
        self.product_table.column("status", width=90)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(ProductFrame1, text="Note:Enter 0 quantity to remove product from the Cart",
                         font=("goudy old style", 12), anchor='w', bg="white", fg="red").pack(side=BOTTOM, fill=X)

        # ===============CUSTOMER FRAME====================
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)
        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 15), bg="lightgray").pack(
            side=TOP, fill=X)

        lbl_name = Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman", 13),
                         bg="lightyellow").place(x=80, y=35, width=180)

        lbl_contact = Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white").place(x=270, y=35)

        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 13),
                        bg="lightyellow").place(x=380, y=35, width=140)

        #== == == =CAL CART FRAME == == ==

        cal_cart_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        cal_cart_frame.place(x=420, y=190, width=530, height=360)

        # =======CALCULATOR FRAME======

        self.var_cal_input = StringVar()

        cal_frame = Frame(cal_cart_frame, bd=4, relief=RIDGE, bg="white")
        cal_frame.place(x=5, y=10, width=268, height=340)

        self.txt_cal_input = Entry(cal_frame, textvariable=self.var_cal_input, font=('arial', 15, 'bold'), width=22,
                                   bd=9, relief=GROOVE, state='readonly', justify=RIGHT)
        self.txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(cal_frame, text='7', font=('arial', 15, 'bold'),command=lambda: self.get_input(7), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=1, column=0)
        btn_8 = Button(cal_frame, text='8', font=('arial', 15, 'bold'),command=lambda: self.get_input(8), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=1, column=1)
        btn_9 = Button(cal_frame, text='9', font=('arial', 15, 'bold'),command=lambda: self.get_input(9), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=1, column=2)
        btn_sum = Button(cal_frame, text='+', font=('arial', 15, 'bold'), command=lambda: self.get_input('+'), bd=5,
                         width=4, pady=13, cursor="hand2").grid(row=1, column=3)

        btn_4 = Button(cal_frame, text='4', font=('arial', 15, 'bold'),command=lambda: self.get_input(4), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=2, column=0)
        btn_5 = Button(cal_frame, text='5', font=('arial', 15, 'bold'),command=lambda: self.get_input(5), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=2, column=1)
        btn_6 = Button(cal_frame, text='6', font=('arial', 15, 'bold'),command=lambda: self.get_input(6), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=2, column=2)
        btn_sub = Button(cal_frame, text='-', font=('arial', 15, 'bold'),command=lambda: self.get_input('-'), bd=5,
                         width=4, pady=13, cursor="hand2").grid(row=2, column=3)

        btn_1 = Button(cal_frame, text='1', font=('arial', 15, 'bold'),command=lambda: self.get_input(1), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=3, column=0)
        btn_2 = Button(cal_frame, text='2', font=('arial', 15, 'bold'),command=lambda: self.get_input(2), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=3, column=1)
        btn_3 = Button(cal_frame, text='3', font=('arial', 15, 'bold'),command=lambda: self.get_input(3), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=3, column=2)
        btn_mul = Button(cal_frame, text='*', font=('arial', 15, 'bold'),command=lambda: self.get_input('*'), bd=5,
                         width=4, pady=13, cursor="hand2").grid(row=3, column=3)

        btn_0 = Button(cal_frame, text='0', font=('arial', 15, 'bold'),command=lambda: self.get_input(0), bd=5,
                       width=4, pady=13, cursor="hand2").grid(row=4, column=0)
        btn_c = Button(cal_frame, text='c', font=('arial', 15, 'bold'),command=self.clear_cal, bd=5, width=4, pady=13,
                       cursor="hand2").grid(row=4, column=1)
        btn_eq = Button(cal_frame, text='=', font=('arial', 15, 'bold'),command=self.perform_cal, bd=5, width=4,
                        pady=13, cursor="hand2").grid(row=4, column=2)
        btn_div = Button(cal_frame, text='/', font=('arial', 15, 'bold'),command=lambda: self.get_input('/'), bd=5,
                         width=4, pady=13, cursor="hand2").grid(row=4, column=3)


        # =======CART FRAME======

        cart_frame = Frame(cal_cart_frame, bd=9, relief=RIDGE)
        cart_frame.place(x=280, y=8, width=245, height=342)
        self.cartTitle = Label(cart_frame, text=" Cart\tTotal Items: [0]", font=("goudy old style", 15), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_frame, columns=("pid", "name", "price", "qty"),
                                       yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid", text="PID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")

        self.CartTable["show"] = "headings"

        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=50)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # =======ADD CART BUTTONS FRAME=======

        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgetsFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Product Name", font=("times new roman", 15), bg="white").place(
            x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15),
                           bg="lightyellow", state='readonly').place(x=5, y=35, width=190, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price Per QTY: ", font=("times new roman", 15),
                            bg="white").place(x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15),
                            bg="lightyellow", state='readonly').place(x=230, y=35, width=150, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity: ", font=("times new roman", 15), bg="white").place(
            x=390, y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),
                          bg="lightyellow").place(x=390, y=35, width=120, height=22)

        self.lbl_instock = Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
        self.lbl_instock.place(x=5, y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman", 15,"bold"), bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add | Update", command=self.add_update_cart,font=("times new roman", 15, "bold"),bg="orange",cursor="hand2").place(x=340, y=70, width=180, height=30)



        # ==========BILLING AREA===========


        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=953, y=111, width=410, height=410)

        bTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#f44336",
                       fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)


        # ==========BILLING BUTTONS==============
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=953, y=521, width=410, height=140)

        self.lbl_amt = Label(billMenuFrame, text="Bill Amount\n[0]", font=("goudy old style", 15, "bold"), bg="#3f51b5",
                             fg="white")
        self.lbl_amt.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billMenuFrame, text="Discount \n[5%]", font=("goudy old style", 15, "bold"),
                                  bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Pay\n[0]", font=("goudy old style", 15, "bold"), bg="#607d8b",
                                 fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(billMenuFrame, text="Print",command=self.print_bill ,font=("goudy old style", 15, "bold"), bg="lightgreen",
                           fg="white", cursor="hand2")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text="Clear ALL", command=self.clear_all,font=("goudy old style", 15, "bold"), bg="gray",
                               fg="white", cursor="hand2")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, text="Generate/Save Bill", command=self.generate_bill,font=("goudy old style", 12, "bold"),
                              bg="#009688", fg="white", cursor="hand2")
        btn_generate.place(x=246, y=80, width=160, height=50)

        # =========footer===========
        footer = Label(self.root,
                       text="Inventory Management System ||  DEVELOPED By ME \n For any Queries please visit: anuvab.xd@gmail.com",
                       font=("times new roman", 11), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)
        self.show()
        #self.bill_top()
        self.update_date_time()

    # =========ALL Functions=================

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))
    #====Show function=============
    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            #self.product_table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"),
            #                                  yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

            cur.execute("Select pid , name , price , qty , status from product where status='Active'")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:

            if self.var_search.get() == "":
                messagebox.showerror("Error", "Select Search Input is required", parent=self.root)
            else:
                cur.execute("select pid , name , price , qty , status from product where name  LIKE '%" + self.var_search.get() + "%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found !!!")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']
        # pid,name,price,qty,stock
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])


    def add_update_cart(self):
        if self.var_pid.get() == '' :
            messagebox.showerror("Error", "Please Select product from the list", parent=self.root)
        elif self.var_qty.get()=='' :
            messagebox.showerror("Error","Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()) :
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)

        else:

            #price_cal=int(self.var_qty.get())*float(self.var_price.get())
            #price_cal=float(price_cal)
            #print(price_cal)
            price_cal=self.var_price.get()
            #pid,name,price,qty,stock

            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]

            #print(self.cart_list)

            # =============Update Cart==============
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ +=1
            #print(present,index_)
            if present == 'yes':
                op = messagebox.askyesno("Confirm",
                                         "Product already present\nDo you want to Update/Remove from the cart list",
                                         parent=self.root)
                if op == True:
                    if self.var_qty.get() == '0':
                        self.cart_list.pop(index_)
                    else:
                        #print(self.var_qty)
                        # pid,name,price,qty,status
                        #self.cart_list[index_][2] = price_cal  # price
                        self.cart_list[index_][3] = self.var_qty.get()  # qty
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amt = 0
        self.net_pay = 0
        self.discount=0

        for row in self.cart_list:
            # pid,name,price,qty,stock
            self.bill_amt = self.bill_amt + (float(row[2])*int(row[3]))

        self.discount=(self.bill_amt * 5) / 100
        self.net_pay = self.bill_amt - self.discount
        self.lbl_amt.config(text=f'Bill Amt:\n{str(self.bill_amt)}')
        self.lbl_net_pay.config(text=f'Net Amt(Rs.)\n{str(self.net_pay)}')
        self.cartTitle.config(text=f" Cart\tTotal Items: [{str(len(self.cart_list))}]")


    def show_cart(self):

        try:
            # self.product_table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"),
            #                                  yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)


            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error", f"Customer Details are required", parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", f"Please add Product to the Cart!!!", parent=self.root)
        else:
            # ===Bill Top=====
            self.bill_top()
            # ===Bill Middle=====
            self.bill_middle()
            # ===Bill Bottom=====
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo("Saved","Bill has been generated Successfully!!!",parent=self.root)
            self.chk_print=1
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        #print(invoice)
        bill_top_temp=f'''
\t\tPrabhuStore-Inventory
\t Phone No. 9163****10,Kolkata-700014
{str("="*46)}
Customer Name: {self.var_cname.get()}
Phone Number: {self.var_contact.get()}
Bill No.: {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
Product Name: \t\t\tQTY: \tPrice: 
{str("="*46)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*46)}
Bill Amount\t\t\t\tRs.{self.bill_amt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*46)}\n
        
        '''
        self.txt_bill_area.insert( END, bill_bottom_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:

            # pid,name,price,qty,stock
            for row in self.cart_list:

                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"

                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+row[3]+"\tRs."+price)
                #=====Update qty in product table==============
                cur.execute("Update product set qty=?,status=? where pid=?", (
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f" Cart\tTotal Items: [0]")
        self.var_search.set('')
        self.chk_print=0
        self.clear_cart()
        self.show()
        self.show_cart()



    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing",parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showerror("Error!","Please generate a bill!!!",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()