from flask_restful import Resource, reqparse

hoteis = [
    {
    'hotel_id': 'alpha',
    'nome': 'Alpha Hotel',
    'estrelas': 4.3,
    'diaria': 420.34,
    'cidade': 'Rio de Janeiro'
    },
    {
    'hotel_id': 'bravo',
    'nome': 'Bravo Hotel',
    'estrelas': 4.4,
    'diaria': 380.90,
    'cidade': 'Santa Catarina'
    },
    {
    'hotel_id': 'charlie',
    'nome': 'Charlie Hotel',
    'estrelas': 3.9,
    'diaria': 320.20,
    'cidade': 'Santa Catarina'
    }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis' : hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    #verifica se existe um hotel
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if(hotel['hotel_id'] == hotel_id):
                return hotel
        return None

    #lista de todos os hoteis
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404 #not found

    #inserir um novo hotel
    def post(self, hotel_id):

        dados = Hotel.argumentos.parse_args()

        novo_hotel = { 'hotel_id': hotel_id, **dados}

        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        novo_hotel = { 'hotel_id': hotel_id, **dados} # **dados é uma forma de desembrulhar os dados passados

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200 # ok

        hoteis.append(novo_hotel)
        return novo_hotel, 201 # created criado

    def delete(self, hotel_id):
        pass
