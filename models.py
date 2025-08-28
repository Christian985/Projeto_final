from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///produtos.sqlite3')

# Gerencia as sessões com o Banco de Dados
db_session = scoped_session(sessionmaker(bind=engine))

# Base_declarativa - Ela permite que você defina Classes Python que representam tabelas de
# Banco de Dados de forma declarativa, sem a necessidade de configurar manualmente a
# relação entre as Classes e as Tabelas.
Base = declarative_base()
Base.query = db_session.query_property()


# Dados da Lista
class Produtos(Base):
    __tablename__ = 'Produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, index=True)
    categoria = Column(String(100), nullable=False, index=True)

    # Representação de Classe
    def __repr__(self):
        return '<User: {} {} >'.format(self.nome,
                                          self.categoria
                                          )

    # Função para Salvar no Banco
    def save(self):
        db_session.add(self)
        db_session.commit()

    # Função para Deletar no Banco
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    # Coloca os Dados na Tabela
    def serialize(self):
        dados_user = {
            'nome': self.nome,
            'categoria': self.categoria,
        }
        return dados_user


# Método para criar Banco
def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
