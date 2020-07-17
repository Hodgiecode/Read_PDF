from flask import Flask
import pdfplumber
import fitz

from flask import request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


app = Flask(__name__)


@app.route('/myfunc',methods=['GET', 'POST'])


def myfunc():
    arg1= request.args.get('book', default = '1', type = str)
    arg2 = request.args.get('src',default = '1', type = str)
    ids=1

    book_name=arg1+".pdf"
    pic_name="pic_"+arg1+"_"+arg2+".png"
    pdf = pdfplumber.open(book_name)

    for i in range(len(pdf.pages)):
        text = pdf.pages[i].extract_text()
        if arg2 in text:
            ids=i
            break

        doc = fitz.open(book_name)
        image_matrix = fitz.Matrix(fitz.Identity)
        image_matrix.preScale(2, 2)
        pix=doc[ids].getPixmap(alpha = False, matrix=image_matrix)
        pix.writePNG(pic_name)

       
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.txt")

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.txt")
    drive = GoogleDrive(gauth)
    file_drive = drive.CreateFile({'parents': [{'id': ["id of directory in Google Drive"]}],'title':pic_name, 'mimeType':'image/png'})
    file_drive.SetContentFile(pic_name)
    file_drive.Upload()
    id_in_gdrive=file_drive['id']

    photo_url="https://docs.google.com/uc?id="+id_in_gdrive
    return photo_url


if __name__ == '__main__':
    app.run()
