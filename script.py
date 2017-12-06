import email
import getpass
import imaplib, os , sys
from tkinter import *
from tkinter import messagebox
top = Tk()
top.title("Gmail Attachment Downloader")
Label(top,text='Enter Your Gmail UserName: ').grid(row=0, column=0)
username = Entry(top)
user =''
username.grid(row=0,column=1, padx=2,pady=2,columnspan=9)

Label(top, text='Enter Your Gmail Password : ').grid(row=1, column=0)
passw = Entry(top, show='*')
password = ''
passw.grid(row=1, column=1, padx=2, pady=2, columnspan=9)

Label(top, text='Enter the Gmail Username of the sender : ').grid(row=2, column=0)
search_e = Entry(top)
search_email = ''

search_e.grid(row=2, column=1, padx=2, pady=2, columnspan=9)

def download():
    curr_dir ='.'
    password = passw.get()
    user = username.get()
    search_email = search_e.get()
    if search_email not in os.listdir(curr_dir):
        os.mkdir(search_email)

    curr_dir = './'+search_email

    m = imaplib.IMAP4_SSL("imap.gmail.com",port=993)
    try :
        m.login(user,password)
    except imaplib.IMAP4.error as e :
        messagebox.showinfo('Error Encountered', "Login failed !!" + str(e) )
        sys.exit(0)


    m.select( mailbox='INBOX') 

    resp, items = m.uid('search', None , 'FROM' , search_email) 
    items = items[0].split() 

    for emailid in items:
        resp, data = m.uid('fetch', emailid , "(RFC822)") 
        raw_email = data[0][1] 
        mail = email.message_from_bytes(raw_email) 
        #body = mail.get_body()
        #print ("["+mail["From"]+"] :" + mail["Subject"])

        if mail.get_content_maintype() != 'multipart':
            continue

        
     
        for part in mail.walk():
           
            if(part.get('Content-Disposition' ) is not None ) :
                filename = part.get_filename()

      

                final_path= os.path.join(curr_dir + filename)

                if not os.path.isfile(final_path) :
          
                   fp = open(curr_dir+"/"+(filename), 'wb')
                   fp.write(part.get_payload(decode=True))
                   fp.close()
    messagebox.showinfo("Download Complete!!", "Done!!")
    m.close()
    m.logout()

Button(top, text='Download', command=download).grid(row=0, column=10, padx=2, pady=2)

Button(top, text='Exit', command=top.destroy).grid(row=1, column=10, padx=2, pady=2)
top.mainloop()


