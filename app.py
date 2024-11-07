from flask import Flask, render_template , redirect,url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os

from pathlib import Path

THIS_FOLDER = Path(__file__).parent.resolve()





# Main.py

def structure_link_and_image():
    result=[]
    with open (THIS_FOLDER/"Urls","r") as f:
        read=f.readlines()
        for index , items in enumerate(read,start=1):
            if "www.google.com" not in items:
                image_name=f"I{index}.png" if os.path.exists(THIS_FOLDER/"static"/f"I{index}.png") else THIS_FOLDER/f"static"/f"I{index}.jpg"
                result.append(f"{image_name} @!@ {items}")
    return result

def get_images(file_name):
    from pypdf import PdfReader

    reader = PdfReader(file_name)
    pages = reader.pages[0]
    for i in pages.images:
        with open (THIS_FOLDER/"static"/i.name , "wb") as f:
            f.write(i.data)

def get_link(file_name):
    import fitz
    doc = fitz.open(file_name)
    pages= doc.load_page(0)
    links = pages.get_links()
    if os.path.exists(THIS_FOLDER/"Urls"):
        os.remove(THIS_FOLDER/"Urls")
        with open (THIS_FOLDER/"Urls","w") as f:
            f.write("")
    for link in links:
        url=link['uri']
        if not url.startswith("https://www.google.com/") :
            with open (THIS_FOLDER/"Urls","a") as f:
                f.write(f"{url}\n")

    # print(links)

def extract_data_from_files(line):
    with open(THIS_FOLDER/"moz_rank.txt","r") as f1:
        read=f1.readlines()
        moz_rank= read[line-1]
        moz_rank=moz_rank.split('\n')[0]
        moz_rank=moz_rank.split('MOZ Rank')[0]
    with open(THIS_FOLDER/"authority.txt","r") as f1:
        read=f1.readlines()
        authority= read[line-1]
        authority=authority.split('\n')[0]
        authority=authority.split('Authority')[0]
    with open(THIS_FOLDER/"global_rank.txt","r") as f1:
        read=f1.readlines()
        global_rank= read[line-1]
        global_rank=global_rank.split('\n')[0]
        global_rank=global_rank.split('Global Rank')[0]
    with open(THIS_FOLDER/"monthly_traffic.txt","r") as f1:
        read=f1.readlines()
        monthly_traffic= read[line-1]
        monthly_traffic=monthly_traffic.split('\n')[0]
        monthly_traffic=monthly_traffic.split('Monthly Traffic')[0]
    with open(THIS_FOLDER/"followers.txt","r") as f1:
        read=f1.readlines()
        followers= read[(line-1)+line]
        followers=followers.split('\n')[0]
        followers=followers.split('Followers')[0]


    return authority , moz_rank , global_rank ,followers, monthly_traffic





# Flask app to upload the file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = THIS_FOLDER/'static'

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(THIS_FOLDER/'input.pdf')
        return redirect(url_for('processing'))
    return render_template('index.html', form=form)

@app.route('/processing',methods=['GET','POST'])
def processing():
    return render_template('processed.html')

@app.route('/result')
def result():
    try:
        dirs= os.listdir(THIS_FOLDER/'static')
        for items in dirs:
            if items != 'input.pdf' and items != 'Line.png':
                os.remove(THIS_FOLDER/f"static"/items)

        path= THIS_FOLDER/'input.pdf'

        print("\nGetting Images")
        get_images(path)                                        # Getting Images Of Brands

        print("\nGetting Links")
        get_link(path)                                          # Getting Links and saving it in Urls

        a='{'
        b='}'
        html_part_1=f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report By EcomRolodex</title>
        <style>
            body {a}
                font-family: 'Montserrat', sans-serif;
                font-size: 20px;
                font-weight: 400;
            {b}
            hr {a}
                border: none;
                border-top: 1px solid #ccc;
                margin: 20px 0;
                padding: 0;
            {b}
            .line {a}
                margin-left: 550px;
                height: auto;
                width: 720px;
            {b}
            .text {a}
                position: relative;
                top: 30px; /* Adjust top spacing */
                left: 50px;
                color: gray;
                bottom: 15px; /* Adjust bottom spacing */
            {b}
            .logo {a}
                position: relative;
                width: 150px;
                height: auto;
                left: 320px;
                top: -30px; /* Adjust top spacing */
                /* bottom: 20px; Adjust bottom spacing */
            {b}
            .letters {a}
                position: relative;
                font-size: 25px;
                top: -80px;
                left: 580px;
                color: #686865;
                white-space: nowrap; /* Prevent line breaks */
            {b}
            .letter {a}
                margin-right: 0px; /* Adjust the space between letters */
            {b}
            .text a, .letter a {a}
                color: #686865; /* Set hyperlink color to inherit from its parent */
                text-decoration: none; /* Remove default underline */
            {b}
            .text a:hover, .letter a:hover {a}
                color: #f70000; /* Change color on hover */
            {b}
        </style>
    </head>
    <body>
        <center><a href="http://www.ecombrandpr.com"><img src="{url_for('static', filename='I1.png')}" alt="logo"></a></center>
        <hr>
        <img src="{url_for('static', filename='Line.png')}" alt="Line" class="line">
        <hr>"""
        html_central_part=''
        html_part_second_last=f""" <div class="letters" style="top: -80px; color: #ccc; font-size: 17px; left: 565px;">
            <span class="letter" style="margin-right: 85px;">Authority</span>
            <span class="letter" style="margin-right: 75px;">MOZ Rank</span>
            <span class="letter" style="margin-right: 60px;">Global Rank</span>
            <span class="letter" style="margin-right: 75px;">Followers</span>
            <span class="letter" style="margin-right: 75px;">Monthly Traffic</span>
        </div>
        <hr>
        """
        html_part_last=f"""
    </body>
    </html>"""
        skip=0

        print("\nManaging links and Images")
        structre_link=structure_link_and_image()                  # Managing Links and Images  (Very Important)

        for index, items in enumerate(structre_link,start=1):
            skip =skip + 1
            if skip== 1:
                pass
            else:
                print("\nGetting data such as MOZ Rank , Global Rank , Authority . . .")
                data= extract_data_from_files(skip-1)

                name=f"I{index}.png" if os.path.exists(THIS_FOLDER/"static"/f"I{index}.png") else f"I{index}.jpg"
                link1=items.split("@!@")[-1]
                if link1.split("//")[-1].startswith("www."):
                    link2=link1.split("www.")[-1].split("/")[0]
                    link=link1.split("www.")[-1].split("/")[0].split(".")[0]
                if not link1.split("//")[-1].startswith("www."):
                    link2=link1.split("https://")[-1].split("/")[0]
                    link=link1.split("https://")[-1].split("/")[0].split(".")[0]
                html_central_part = html_central_part+f"""<p class="text"><a href="{link1}">{link.upper()}</a></p>
        <img src="{url_for('static', filename = name)}" alt="logo" class="logo">
        <div class="letters">
            <span class="letter"><a href="https://moz.com/domain-analysis?site={link2}" style="margin-right: 125px;">{data[0]}</a></span>
            <span class="letter"><a href="https://moz.com/domain-analysis?site={link2}" style="margin-right: 120px;">{data[1]}</a></span>
            <span class="letter"><a href="https://www.similarweb.com/website/{link2}/#overview" style="margin-right: 80px;">{data[2]}</a></span>
            <span class="letter" style="margin-right: 100px;">{data[3]}</span>
            <span class="letter"><a href="https://www.similarweb.com/website/{link2}/#overview">{data[4]}</a></span>
        </div>"""+html_part_second_last

        html_final_content=html_part_1+html_central_part+html_part_last
        return html_final_content
    except Exception as e:
        return(e)




"""<span class="letter">-</span>
        <span class="letter"><a href="https://www.similarweb.com/website/financialcontent.com/#overview">{data[3]}</a></span>
    </div>"""



if __name__ == '__main__':
    app.run(debug=True)
