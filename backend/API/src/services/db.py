from sqlalchemy import create_engine

engine = create_engine('mariadb+mariadbconnector://root:admin@127.0.0.1:3306/innovatieplatform',pool_size=10)