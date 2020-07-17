from flask import Flask
import pdfplumber
import fitz

from flask import request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


app = Flask(__name__)


@app.route('/myfunc',methods=['GET', 'POST'])


def myfunc():
    arg2= request.args.get('book', default = '1', type = str)
    arg3 = request.args.get('id',default = '*', type = str)
    arg4 = request.args.get('exer',default = '1', type = str)
    ids=1

    book_name=arg2+".pdf"
    pic_name="pic_"+arg2+"_"+arg4+".png"
    pdf = pdfplumber.open(book_name)

    for i in range(len(pdf.pages)):
        text = pdf.pages[i].extract_text()
        if arg4+"." in text and i>6:
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
    file_drive = drive.CreateFile({'parents': [{'id': ["19r_Of5Jq80IZSnWg2XinE4vdl2ShiywO"]}],'title':pic_name, 'mimeType':'image/png'})
    file_drive.SetContentFile(pic_name)
    file_drive.Upload()
    id_in_gdrive=file_drive['id']

    photo_url="https://docs.google.com/uc?id="+id_in_gdrive
    url_= 'https://api.telegram.org/bot'+botToken+'/sendMessage?chat_id='+arg3+"&disable_web_page_preview=false&text="+photo_url
    return url_


if __name__ == '__main__':
    app.run()
