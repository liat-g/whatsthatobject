from flask import Flask 
from flask_sqlalchemy import SQLAlchemy ##ORM 
from flask_cors import CORS 
from flask import Flask, request, render_template
import objaverse 
import pandas as pd
# from langchain import OpenAI
# from langchain.chains import ConversationalRetrievalChain
# from langchain.document_loaders import SQLiteDataRetriever
##https://colab.research.google.com/drive/15XpZMjrHXuky0IgBbXcsUtb_0g-XWYmN?usp=sharing#scrollTo=wLB-BPGqGi2e
import objaverse.xl as oxl 
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create a table
c.execute('''CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY, content TEXT, metadata TEXT)''')

conn.commit()
conn.close()

# db_retriever = SQLiteDataRetriever(
#     db_path="data.db",
#     table_name="documents",
#     col_id="id",
#     col_content="content",
#     col_metadata="metadata",
# )

app = Flask(__name__)
CORS(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://mydatabase.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

# db = SQLAlchemy(app) ##db instance

# llm = OpenAI(temperature=0)
# retriever = db_retriever.get_retriever()
# chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever)

uids = objaverse.load_uids()
len(uids), type(uids) 

print(uids[:10]) ##receiving uids 

##need uids to download
def add_model(conn, model): ##db of models
    sql = ''' INSERT INTO model(uri, uid, name, isDownloadable=True, tags, slug,)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, model)
    conn.commit()
    return cur.lastrowid

def add_vector(conn, vec): ##relationally having our vector uid and index together
    sql = '''INSERT INTO vec(uid, idx)
             VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, vec)
    conn.commit()
    return cur.lastrowid

def load_annotations(uids: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
   annotations = {}
   if uids is None:
       uids = objaverse.available_annotations()
   for uid in uids:
       model = uid
       annotations[model] = objaverse.retrieve_annotation(model)
   return annotations


def main():
    try:
        with sqlite3.connect('my.db') as conn:
            # add a new project
            ##add each uid in with the information outlined above
            project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
            for item in annotations:
                   print(item) ##look at each annotation

            model_id = add_model(conn, model)
            print(f'Created a project with the id {model_id}')

            ##add the vectors after langchain queries the db 


    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    main()

