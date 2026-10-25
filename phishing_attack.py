import pandas as pd
import numpy as np
import re
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import tkinter as tk
from sklearn import svm
from PIL import Image, ImageTk
from tkinter import ttk
from joblib import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from nltk.corpus import stopwords
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import pickle
import nltk
from sklearn.ensemble import RandomForestRegressor
import webbrowser

nltk.download('stopwords')
stop = stopwords.words('english')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

root = tk.Tk()
dt = tk.StringVar()
root.configure(background="seashell2")
#root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("phishing website using machine learning")


#430
#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 =Image.open('4.png')
image2 =image2.resize((w,h), Image.ANTIALIAS)

background_image=ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)
# #
lbl = tk.Label(root, text="phishing website using machine learning ", font=('times', 35,' bold '), height=1, width=60,bg="#152238",fg="white")
lbl.place(x=0, y=0)

def shift():
    x1,y1,x2,y2 = canvas.bbox("marquee")
    if(x2<0 or y1<0): #reset the coordinates
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height()//2
        canvas.coords("marquee",x1,y1)
    else:
        canvas.move("marquee", -2, 0)
    canvas.after(1000//fps,shift)

canvas=tk.Canvas(root,bg="#152238")
canvas.pack()
canvas.place(x=0, y=0)
text_var="phishing website using machine learning"
text=canvas.create_text(0,-2000,text=text_var,font=('Raleway',25,'bold'),fill='white',tags=("marquee",),anchor='w')
x1,y1,x2,y2 = canvas.bbox("marquee")
width = 1600
height = 80
canvas['width']=width
canvas['height']=height
fps=40    
shift()   


frame_alpr = tk.LabelFrame(root, text=" --Process-- ", width=300, height=500, bd=5, font=('times', 14, ' bold '),bg="#152238",fg="white")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=20, y=100)

def Data_Display():
    columns = ['domain', 'ranking', 'activeDuration']
    print(columns)

    data1 = pd.read_csv(r"combined_dataset.csv", encoding='unicode_escape')
    data1.shape
    data1.shape
    data1.head()
    data1

    domain = data1.iloc[:, 0]
    ranking = data1.iloc[:, 1]
    activeDuration = data1.iloc[:, 2]

    display = tk.LabelFrame(root, width=600, height=400)
    display.place(x=400, y=100)
    display["borderwidth"] = 15

    tree = ttk.Treeview(display, columns=(
        'domain', 'ranking', 'activeDuration'))

    style = ttk.Style()
    style.configure('Treeview', rowheight=50)
    style.configure("Treeview.Heading", font=("Tempus Sans ITC", 15, "bold italic"))
    style.configure(".", font=('Helvetica', 15), background="blue")
    style.configure("Treeview", foreground='white', background="black")

    tree["columns"] = ("1", "2", "3")
    tree.column("1", width=300)
    tree.column("2", width=200)
    tree.column("3", width=150)

    tree.heading("1", text="domain")
    tree.heading("2", text="ranking")
    tree.heading("3", text="activeDuration")

    treeview = tree
    tree.grid(row=0, column=0, sticky=tk.NSEW)
    print("Data Displayed")

    for i in range(0, 10000):
        tree.insert("", 'end', values=(domain[i], ranking[i], activeDuration[i]))
        i = i + 1
        print(i)

def Train():
    result = pd.read_csv(r"combined_dataset.csv", encoding='unicode_escape')
    result.head()

    result['headline_without_stopwords'] = result['domain'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    def pos(headline_without_stopwords):
        return TextBlob(headline_without_stopwords).tags

    os = result.headline_without_stopwords.apply(pos)
    os1 = pd.DataFrame(os)
    os1.head()
    os1['pos'] = os1['headline_without_stopwords'].map(lambda x: " ".join(["/".join(x) for x in x]))
    result = pd.merge(result, os1, right_index=True, left_index=True)
    result.head()
    result['pos']
    result_train, result_test, label_train, label_test = train_test_split(result['pos'], result['label'], test_size=0.2, random_state=1)

    tf_vect = TfidfVectorizer(lowercase=True, use_idf=True, smooth_idf=True, sublinear_tf=False)

    X_train_tf = tf_vect.fit_transform(result_train)
    X_test_tf = tf_vect.transform(result_test)

    def svc_param_selection(X, y, nfolds):
        Cs = [0.001, 0.01, 0.1, 1, 10]
        gammas = [0.001, 0.01, 0.1, 1]
        param_grid = {'C': Cs, 'gamma': gammas}
        grid_search = GridSearchCV(svm.SVC(kernel='linear'), param_grid, cv=nfolds)
        grid_search.fit(X, y)
        return grid_search.best_params_

    svc_param_selection(X_train_tf, label_train, 5)

    clf = svm.SVC(C=10, gamma=0.001, kernel='linear')
    clf.fit(X_train_tf, label_train)
    pred = clf.predict(X_test_tf)

    with open('vectorizer.pickle', 'wb') as fin:
        pickle.dump(tf_vect, fin)
    with open('mlmodel.pickle', 'wb') as f:
        pickle.dump(clf, f)

    pkl = open('mlmodel.pickle', 'rb')
    clf = pickle.load(pkl)
    vec = open('vectorizer.pickle', 'rb')
    tf_vect = pickle.load(vec)

    X_test_tf = tf_vect.transform(result_test)
    pred = clf.predict(X_test_tf)

    print(metrics.accuracy_score(label_test, pred))
    print(confusion_matrix(label_test, pred))
    print(classification_report(label_test, pred))

    print("=" * 40)
    print("==========")
    print("Classification Report : ", (classification_report(label_test, pred)))
    print("Accuracy : ", accuracy_score(label_test, pred) * 100)
    accuracy = accuracy_score(label_test, pred)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    ACC = (accuracy_score(label_test, pred) * 100)
    repo = (classification_report(label_test, pred))

    label4 = tk.Label(root, text=str(repo), width=35, height=10, bg='khaki', fg='black', font=("Tempus Sanc ITC", 14))
    label4.place(x=205, y=100)

    label5 = tk.Label(root, text="Accuracy : " + str(ACC) + "%\nModel saved as RF_MODEL1.joblib", width=35, height=3, bg='khaki', fg='black', font=("Tempus Sanc ITC", 14))
    label5.place(x=205, y=320)

    dump(clf, "RF_MODEL.joblib")
    print("Model saved as RF_MODEL.joblib")

entry = tk.Entry(frame_alpr, width=24, bg="white", font=("Times New Roman", 16, "italic"))
entry.insert(0, "Enter text here...")
entry.place(x=5, y=90)

def Test():
    predictor = load("RF_MODEL.joblib")
    Given_text = entry.get()
    vec = open('vectorizer.pickle', 'rb')
    tf_vect = pickle.load(vec)
    X_test_tf = tf_vect.transform([Given_text])
    y_predict = predictor.predict(X_test_tf)
    print(y_predict[0])
    if y_predict[0] == 0:
        label4 = tk.Label(root, text="Normal Website", width=30, height=2, bg='#ff9999', fg='black', font=("Tempus Sanc ITC", 14))
        label4.place(x=400, y=500)
        if not Given_text.startswith(('http://', 'https://')):
            Given_text = 'http://' + Given_text
        webbrowser.open(Given_text)
    elif y_predict[0] == 1:
        label4 = tk.Label(root, text="Phishing Website", width=30, height=2, bg='Red', fg='black', font=("Tempus Sanc ITC", 14))
        label4.place(x=400, y=500)

def window():
    root.destroy()

def rosmware():
    from subprocess import call
    call(["python", "rosmware.py"])

button1 = tk.Button(frame_alpr, command=Data_Display, text="Data_Display", bg="sky blue", fg="black", width=24, font=("Times New Roman", 15, "italic", "bold"))
button1.place(x=5, y=30)

button2 = tk.Button(frame_alpr, command=Test, text="Test", bg="sky blue", fg="black", width=24, font=("Times New Roman", 15, "italic", "bold"))
button2.place(x=5, y=180)

button2 = tk.Button(frame_alpr, command=rosmware, text="Rosmware", bg="sky blue", fg="black", width=24, font=("Times New Roman", 15, "italic", "bold"))
button2.place(x=5, y=300)

button3 = tk.Button(frame_alpr, text="Exit", command=window, bg="red", fg="black", width=24, font=("Times New Roman", 15, "italic", "bold"))
button3.place(x=5, y=390)

root.mainloop()
