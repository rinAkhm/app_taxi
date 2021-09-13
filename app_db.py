from sqlalchemy import Column, create_engine, VARCHAR, Boolean, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from sqlalchemy_utils import ChoiceType

engine = create_engine('postgresql://postgres:1234@127.0.0.1:5432/app_taxi')
Model = declarative_base()


class Driver(Model):  # type: ignore
    """Модель таблицы Водители."""
    __tablename__ = 'drivers'  # имя таблицы

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID driver")
    name = Column(VARCHAR(50), nullable=False, comment="name driver")
    car = Column(VARCHAR(50), nullable=False, comment="driver car")

    @property
    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'car': self.car
        }


class Client(Model):
    """Модель таблицы клиенты."""
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID client")
    name = Column(VARCHAR(50), nullable=False, comment="name client")
    is_vip = Column(Boolean, nullable=False, comment="status vip")

    @property
    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'is_vip': self.is_vip
        }


class Order(Model):
    """Модель таблицы заказы."""
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID order")
    address_from = Column(VARCHAR(100), nullable=False, comment="order address")
    address_to = Column(VARCHAR(100), nullable=False, comment="arrival address")
    driver_id = Column(Integer, ForeignKey('drivers.id', ondelete="SET DEFAULT"),
                       nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete="SET DEFAULT"),
                       nullable=False)
    date_created = Column(TIMESTAMP, nullable=False, comment="date create order")
    status = Column(ChoiceType([('not_accepted', 'not_accepted'),
                                ('in_progress', 'in_progress'),
                                ('done', 'done'),
                                ('cancelled', 'cancelled')], impl=VARCHAR()),
                    nullable=False, comment='status orders')
    driver = relationship("Driver", foreign_keys=[driver_id])
    client = relationship("Client", foreign_keys=[client_id])

    @property
    def serialize(self) -> dict:
        return {'id': self.id,
                'address_from': self.address_from,
                'address_to': self.address_to,
                'driver_id': self.driver_id,
                'client_id': self.client_id,
                'date_created': self.date_created,
                'status': self.status}


if __name__ == "__main__":
    Model.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    session.close()
