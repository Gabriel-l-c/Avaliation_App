from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#sempre que criar alteracoes aqui deve ser feio makemigrations end migrate

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name




class Room(models.Model):

    ## ---- relacionamentos com as outras classes
    host= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    
    
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True) #adiciona usuarios nat r

    #---- aqui salva o ultimo update do objeto (rastreamento do ultimo update)
    updated= models.DateTimeField(auto_now =True)
    # ---- aqui e 'fixo' coloca uma date e time na ccriacao do objetp
    created = models.DateTimeField(auto_now_add =True)
    
    #ordenar os field/coteudos  em termos dos updateds e createds 
    class Meta:
        ordering =['-updated', '-created']

    def __str__(self):

        return str(self.name)
 #EXEMPLO DE RELACIONAMENTOS
    
class Message(models.Model):
    
    #
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    #OQUE IRA ACONTECER COM TODAS AS INTACIAS DO OBJETO ? CASCADE == DELETA TUDO
    #EXEMPLO== DELETAR A CONTA DO TWIITER
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
       #---- aqui salva o ultimo update do objeto (rastreamento do ultimo update)
    updated= models.DateTimeField(auto_now =True)
    # ---- aqui e 'fixo' coloca uma date e time na ccriacao do objetp
    created = models.DateTimeField(auto_now_add =True)
    

   
    class Meta:
        ordering =['-updated', '-created']


    def __str__(self):
        #retornar apenas ao primeitos 50 caracteres
        return self.body[0:50]
