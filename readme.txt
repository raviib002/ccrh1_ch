Python == 3.7+
Django==2.2
django-cms==3.7.1
django-debug-toolbar==2.2
Internationalization/Locale - English & Hindi
Model Audit Logs (Model Auditing)
fhir.resources-5.0.1



TO DO LIST
---------------------
https://pypi.org/project/fhir.resources/ - FHIR 
Multiple DB - POC
Internationalization/Locale - Rules & guidelines to be define
Logger/Track changes done by individual - To be indentified (POC)


***********************Internationalize Templates***************************
Then you have to mark all strings which have to be translated. Suppose you have the following template file
<h1>Welcome to our site!</h1>
<p>Here you find polls.</p>
This file needs to be adapted to look like this:
<h1>{% trans 'WelcomeHeading' %}</h1>
<p>{% trans 'WelcomeMessage' %}</p>

************************Internationalize Inside Python Code******************************
from django.utils.translation import ugettext as _
def index(request):
    output = _('StatusMsg')
    return HttpResponse(output)
    
    
*********************Create Translation Files*******************************
$ django-admin makemessage -l hi
msgid "WelcomeMessage"
msgstr ""
When you have finished translating, you have to compile everything by running the following: 
$ django-admin compilemessages

#REMOVED AFTER MONGODB INSTALLATION- REFERENCE
django-mongodb-engine==0.6.0
django-mongodb-engine-py3==0.6.0.1
django-mongokit==0.2.6
mongokit==0.9.1.1