# Basic Many to many relationship with Python and SQLAlchemy
# Author: Fabrício G. M. de Carvalho, Ph.D
##

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey

# Uma engine gerencia a comunicação com o banco de dados que é feita a partir
# da aplicação. Desativar o "True" quando entrar em produção.
engine = create_engine('mysql+pymysql://root:root@localhost/python_orm', echo=False) #deixar echo True só durante debug

# Não utilizar comandos diretos a partir de engine, tais como o exemplo abaixo.
# Isso quebra o propósito do ORM e torna a aplicação mais dependente, no código-fonte, da sintaxe do DBMS

#engine.execute("CREATE TABLE USUARIOS ( id int NOT NULL AUTO_INCREMENT, nome varchar(100), PRIMARY KEY (id) );")
#engine.execute("INSERT INTO USUARIOS (nome) VALUES  ('PEDRO')")


Session = sessionmaker(bind=engine)
session = Session()

db = declarative_base()


usuario_telefone = Table('usuario_telefone', db.metadata,
    Column('usuario_id', ForeignKey('usuarios.id'), primary_key=True),
    Column('telefone_id', ForeignKey('telefones.id'), primary_key=True)
)

class Usuario(db):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    telefones = relationship("Telefone", secondary=usuario_telefone)

    def __repr__(self):
        return f'Usuário {self.nome}'


class Telefone(db):
    __tablename__ = 'telefones'

    id = Column(Integer, primary_key=True)
    numero = Column(String(100))

    def __repr__(self):
        return f'Telefone {self.numero}'


#db.metadata.create_all(engine)  # Essa linha só deve ser executada no momento da criação da base de dados (primeira execução)

usuario_1 = Usuario()
usuario_1.nome = "Fabrício GMC"
usuario_2 = Usuario()
usuario_2.nome = "Thales GMC"
telefone_1 = Telefone(numero = "2222222")
telefone_2 = Telefone(numero =  "333333")
usuario_1.telefones.append(telefone_1)
usuario_1.telefones.append(telefone_2)
usuario_2.telefones.append(telefone_1)

session.add(usuario_1)  #Apenas prepara para tornar permanente a transação
session.add(usuario_2)
session.commit()    #Torna a transação do BD permanente
consulta = session.query(Usuario).filter(Usuario.nome.like('%Fab%')).all()
print("Usuário: ...")
for resultado in consulta:
    print('Nome: ' + str(resultado))
    for telefone in resultado.telefones:
        print(telefone)
session.close()
