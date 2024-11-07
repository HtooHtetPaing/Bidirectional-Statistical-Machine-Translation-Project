from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
import os
from django.conf import settings
import shutil

# Create your views here.
def translator(request):
    template = loader.get_template('index.html')
    context={
	'curlink':'firstPage'
	}
    #return render(request, 'index.html', context)
    return HttpResponse(template.render(context,request))

def saveinfo(request):
    if request.method == 'POST':
        input = request.POST.get('txt1',None)
        rad = request.POST.get('rad',None)
        appdir = os.path.join(settings.BASE_DIR,'translator/')
        
        print("Directory",appdir)
        print(rad)
        if rad=='option1':
            #***from Myanmar to English***#
            #deleting filtered ahead\
            if(os.path.isdir(appdir+'myanmarfiltered')):
                shutil.rmtree(appdir+'myanmarfiltered')

            #writing data into text file
            with open(appdir+'inputmyanmar.txt','w',encoding='utf-8') as f:
                f.write(input+"\n")

            #tokenize 
            #python sylbreak.py --input /home/htoohtetpaing/smt/inputtest.txt --separator " " --output /home/htoohtetpaing/smt/output.txt
            cmdtokenize = 'python '+appdir+'sylbreak.py --input '+appdir+'inputmyanmar.txt --separator " " --output '+appdir+'outmyanmarclean.txt'
            os.system(cmdtokenize)

            #filter
            #/home/htoohtetpaing/smt/mosesdecoder/scripts/training/filter-model-given-input.pl filtered /home/htoohtetpaing/smt/MyEn/tuning/mert/moses.ini /home/htoohtetpaing/smt/MyEn/data/test.clean.my
            cmdfilter = "/home/htoohtetpaing/smt/mosesdecoder/scripts/training/filter-model-given-input.pl "+appdir+"myanmarfiltered /home/htoohtetpaing/smt/MyEn/tuning/mert/moses.ini "+appdir+"outmyanmarclean.txt"
            os.system(cmdfilter)

            #decode
            #nohup nice /home/htoohtetpaing/smt/mosesdecoder/bin/moses -f /home/htoohtetpaing/smt/MyEn/filtered/moses.ini < /home/htoohtetpaing/smt/MyEn/data/test.clean.my > translated.en 2> newstest.out
            cmddecode = "nohup nice /home/htoohtetpaing/smt/mosesdecoder/bin/moses -f "+appdir+"myanmarfiltered/moses.ini < "+appdir+"outmyanmarclean.txt > "+appdir+"translated.en 2> "+appdir+"newstest.out"
            os.system(cmddecode)
            
            #normalization
            #/home/htoohtetpaing/smt/mosesdecoder/scripts/tokenizer/escape-special-chars.perl
            cmdnormalize = "/home/htoohtetpaing/smt/mosesdecoder/scripts/tokenizer/escape-special-chars.perl -l en < "+appdir+"translated.en > "+appdir+"normalized.txt"
            os.system(cmdnormalize)
            with open(appdir+'normalized.txt','r',encoding='utf-8') as f:
                result = f.read()
            data = {'inputText':result}
            return JsonResponse(data)
        else:
            #**English to Myanmar**#
            ##deleting filtered ahead\
            if(os.path.isdir(appdir+'englishfiltered')):
                shutil.rmtree(appdir+'englishfiltered')

            #writing data into text file
            with open(appdir+'inputEnglish.txt','w',encoding='utf-8') as f:
                f.write(input+"\n")
            #tokenize
            cmdtokenize = "/home/htoohtetpaing/smt/mosesdecoder/scripts/tokenizer/tokenizer.perl -l en < "+appdir+"inputEnglish.txt > "+appdir+"outenglishclean.txt"
            os.system(cmdtokenize)

            #loweracse
            cmdlower = "/home/htoohtetpaing/smt/mosesdecoder/scripts/tokenizer/lowercase.perl -l en < "+appdir+"outenglishclean.txt > "+appdir+"outenglishlower.txt"
            os.system(cmdlower)

            #filter
            #/home/htoohtetpaing/smt/mosesdecoder/scripts/training/filter-model-given-input.pl filtered /home/htoohtetpaing/smt/EnMy/tuning/mert/moses.ini /home/htoohtetpaing/smt/EnMy/data/test.clean.en
            cmdfilter = "/home/htoohtetpaing/smt/mosesdecoder/scripts/training/filter-model-given-input.pl "+appdir+"englishfiltered /home/htoohtetpaing/smt/EnMy/tuning/mert/moses.ini "+appdir+"outenglishlower.txt"
            os.system(cmdfilter)

            #decode
            #nohup nice /home/htoohtetpaing/smt/mosesdecoder/bin/moses -f /home/htoohtetpaing/smt/EnMy/filtered/moses.ini < /home/htoohtetpaing/smt/EnMy/data/test.clean.en > translated.my 2> newstest.out
            cmddecode = "nohup nice /home/htoohtetpaing/smt/mosesdecoder/bin/moses -f "+appdir+"englishfiltered/moses.ini < "+appdir+"outenglishlower.txt > "+appdir+"translated.my 2> "+appdir+"newstest.out"
            os.system(cmddecode)
            
            with open(appdir+'translated.my','r',encoding='utf-8') as f:
                result = f.read()
    
            data = {'inputText':result}
            return JsonResponse(data)
    
