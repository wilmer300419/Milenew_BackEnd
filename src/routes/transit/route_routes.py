from flask import request, jsonify

from src.routes.crud_blueprint import crud_blueprint
from src.security.auth_middleware import token_required
from src.security.permissions import admin_required
from src.services.transit.route_service import RouteService

service = RouteService()
route_bp = crud_blueprint("route", "/api/routes", service, "Ruta")


# ---- Estaciones de la ruta (con su orden de parada) ----
@route_bp.get("/<int:id_route>/stations")
@token_required
def list_route_stations(id_route):
    return jsonify(service.list_stations(id_route)), 200


@route_bp.post("/<int:id_route>/stations")
@token_required
@admin_required
def add_route_station(id_route):
    return jsonify(service.add_station(id_route, request.get_json(silent=True))), 201


@route_bp.put("/<int:id_route>/stations/<int:id_station>")
@token_required
@admin_required
def update_route_station(id_route, id_station):
    return jsonify(service.update_station_order(id_route, id_station, request.get_json(silent=True))), 200


@route_bp.delete("/<int:id_route>/stations/<int:id_station>")
@token_required
@admin_required
def remove_route_station(id_route, id_station):
    service.remove_station(id_route, id_station)
    return jsonify({"message": f"Estacion {id_station} quitada de la ruta {id_route}."}), 200


# ---- Buses asignados a la ruta (por fecha de servicio AAAA-MM-DD) ----
@route_bp.get("/<int:id_route>/buses")
@token_required
def list_route_buses(id_route):
    return jsonify(service.list_buses(id_route)), 200


@route_bp.post("/<int:id_route>/buses")
@token_required
@admin_required
def assign_route_bus(id_route):
    return jsonify(service.assign_bus(id_route, request.get_json(silent=True))), 201


@route_bp.put("/<int:id_route>/buses/<int:id_bus>/<service_date>")
@token_required
@admin_required
def update_route_bus(id_route, id_bus, service_date):
    return jsonify(service.update_bus_assignment(id_route, id_bus, service_date, request.get_json(silent=True))), 200


@route_bp.delete("/<int:id_route>/buses/<int:id_bus>/<service_date>")
@token_required
@admin_required
def remove_route_bus(id_route, id_bus, service_date):
    service.remove_bus_assignment(id_route, id_bus, service_date)
    return jsonify({"message": f"Bus {id_bus} desasignado de la ruta {id_route} ({service_date})."}), 200
