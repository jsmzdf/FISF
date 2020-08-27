#-------------------------------------------------------------------------------
# Name:        Modulo Otro
# Purpose:     Sacarle nota a Daza 2(.(w/4))
#
# Author:      Alguien diferente
#
# Created:     19/09/1999
# Copyright:   (TM) ays 2021(?)
# Licence:     <uranus>
#-------------------------------------------------------------------------------

#importe de librerias
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from app import db

# definicion tabla usuario
class usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    __table_args__ = tuple(
        db.CheckConstraint("nom_usu ~* '^[A-Za-z]+$'")
        )
    id_usu = db.Column(db.Integer, primary_key=True, nullable=False)
    nom_usu = db.Column(db.String(200), nullable=False)
    ape_usu = db.Column(db.String(200), nullable=False)
    contra_usu = db.Column(db.String(200), nullable=False)
    email_usu = db.Column(db.String(300), unique=True, nullable=False)
    proyecto_usu = db.Column(db.String(300), nullable=False)
    codigo_usu = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, nom: str, apel: str, passs: str, mail: str,  proyc: str,  codi: str):
        '''
        Objeto en base de datos usuario
        Parametros:
            nom (str): Cadeda unica que identifica al usuario
            pass (str): Clave del usuario para poder acceder a su registro
        '''
        self.nom_usu = nom
        self.ape_usu = apel
        self.contra_usu = passs
        self.email_usu = mail
        self.proyecto_usu = proyc
        self.codigo_usu = codi

    def __repr__(self) -> str:
        '''
        Representacion en forma de cadena que retornara al solicitar un usuario
        Retorno:
            Cadena de caracteres con el nombre unico del usuario
        '''
        return f"[Usuario {self.nom_usu}]"

    @property
    def id(self):
        return self.id_usu

    def get_id(self):
        return self.id_usu

    '''@property
    def clave(self):
        raise AttributeError('La clave no es un atributo leible')

    @clave.setter
    def clave(self, passs):
        self.contra_usu = passs'''

    @staticmethod
    def getField():
        return ["nom_usu", "ape_usu", "contra_usu", "email_usu",
                "proyecto_usu", "codigo_usu"]