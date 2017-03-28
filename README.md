# WebSemantica1
Primeiro trabalho de web semantica
___________________________
Django - Informação basica|
---------------------------
Criar Pagina |
--------------
Na pagina urls.py acrescentar a seguinte linha:
	- url(r'^*nome da pagina que se quer criar (sem o '*')*$', app.views.*nome da pagina que se quer criar (sem o '*')*, name='*nome da pagina que se quer criar (sem o '*')*'),

Na pagina views.py criar uma view para a paginta, a seguir encontra-se um codigo exemplo:
def *Nome da pagina*(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/*Nome da pagina*',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

Na pagina layout.html inserir a seguinte linha no local das paginas para se conseguir ter acesso à pagina:
<li><a href="{% url '*Nome da pagina*' %}">*Nome da pagina*</a></li>
---------------
Base de dados |
-------------------
Connectar a SQLite |
-------------------
No ficheiro Settings.py adcionar em ALLOWED_HOSTS 'localhost'
Caso não tenha este campo, adcionar as configurações de base de dados sqlite:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
-------------------------------
Criar tabelas à base de dados |
-------------------------------
no ficheiro models.py cria-se classes com o nome da tabela que se pretende, exemplo:
class Line(models.Model):                    # model - class    - table
    id = models.IntegerField
    idTe = models.CharField(max_length=3)
    texto = models.CharField(max_length=255)  # field - instance - row
    def __str__(self):
        return self.id
Com esta função irá ser criada uma tabela de nome "Line" com as colunas id, idTe e texto.
Para "injectar" as tabelas na base de dados tem de correr os seguintes comandos na linha de comandos na pasta do projecto:
1º comando: python .\manage.py makemigrations
2º comando: pythin .\manage.py migrate
