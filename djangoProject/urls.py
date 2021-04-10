"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import base64

import pdfplumber
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from rest_framework import serializers
from rest_framework.views import APIView


class Serializers(serializers.ModelSerializer):
    name = serializers.CharField()
    encoded = serializers.CharField()

    class Meta:
        fields = ['name', 'encoded']

import docx
class FilesF(APIView):
    def post(self, request):
        order_list = request.POST.getlist('title')
        pdftext = []
        order = []
        for i in order_list:
            order.append(i.split(','))

        index = 0
        for i in order:
            print(i[1])
            if "pdf" in i[2]:
                n = str(i[0])
                d = base64.b64decode(n)
                filename = 'testpdf' + str(index)
                with open(filename, 'wb') as pdf:
                    pdf.write(d)
                with pdfplumber.open(r'{}'.format(filename)) as pdf:
                    sdfp = []
                    for j in pdf.pages:
                        sdfp.append(j.extract_text()[:10])
                        # print(j.extract_text())
                    pdftext.append('pdf'+"".join(sdfp))
            else:
                n = str(i[0])
                d = base64.b64decode(n)
                filename = 'testdoc' + str(index) #+ ".docx"
                with open(filename, 'wb') as pdf:
                    pdf.write(d)
                doc = docx.Document(filename)
                sdfp = []
                for i in doc.paragraphs:
                    # print(i.text)
                    sdfp.append(i.text[:10])
                pdftext.append("doc" + "".join(sdfp))
            index += 1

            # print(len(order_))
        # for i in order_list:
        #     print(i)
        # types = request.POST.getlist('type')
        # print(types)
        # n = str(order_list[0])
        # d = base64.b64decode(n)
        # fds = []
        # for i in order_list:
        #     print(i.get('type'))
        # index = 0
        # for i in order_list:
        #     n = str(order_list[0])
        #     d = base64.b64decode(n)
        #     filename = 'tessdft'+ str(index)
        #     with open(filename, 'wb') as pdf:
        #         pdf.write(d)
        #     import pdfplumber
        #     with pdfplumber.open(r'{}'.format(filename)) as pdf:
        #         first_page = pdf.pages[0]
        #         print(len(pdf.pages))
        #         dsfg = first_page.extract_text()
        #     fds.append(dsfg[:50])
        #     index += 1

        return JsonResponse({"success": True, "message": "Message", "list": [
            {
                "name": "Name",
                "count": 17,
                "sentences": [
                    {"page": 1, "text": "Texxt1"},
                    {"page": 2, "text": "Texxt2"},
                    {"page": 3, "text": "Texxt3"}
                ]
            }
        ]}, safe=False)


def get_he(request):
    if request.method == "POST":
        files = request.FILES
        info = request.POST['sender_information']
        print(files)
        print(info)
        return JsonResponse({"success": True, "message": "sad"}, safe=False)
    return JsonResponse({"status": "asd"}, safe=False)


class uploadfile(APIView):
    def post(self, request):
        print(request.POST)
        print(request.FILES)
        myfiles = request.FILES['filename']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        for i in myfiles:
            print(i)

        return JsonResponse({"success": True, "message": "sad"}, safe=False)


class FilesdF(APIView):
    def post(self, request):
        order_list = request.POST.getlist('files')
        key = request.POST.get('key')
        print(order_list)
        print(key)
        return JsonResponse({"success": True, "message": "sad"}, safe=False)

from files.views import sdfk
urlpatterns = [
    # path('gets/', FileF.as_view() ),
    path('posts', sdfk.as_view()),
    path('post', sdfk.as_view()),
    path('uploadfile', uploadfile.as_view()),
    path('admin/', admin.site.urls),
]
