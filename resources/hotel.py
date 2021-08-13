from flask_restful import Resource, reqparse
from models.hotel import HotelModel

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
        return {'hoteis' : [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type=str, required=True, help="the field 'nome' cannot be left blank")
    atributos.add_argument('estrelas', type=float, required=True, help="the field 'estrelas' cannot be left blank")
    atributos.add_argument('diaria')
    atributos.add_argument('cidade')



    #lista de um hotel com id especifico
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404 #not found

    #inserir um novo hotel
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' alread exists".format(hotel_id)}, 400
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # internal server error
        return hotel.json()

    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 # ok
        hotel = HotelModel(hotel_id, **dados)

        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500 # internal server error
        return hotel.json(), 201 # created criado

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'an error ocurred trying to delete hote'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404
