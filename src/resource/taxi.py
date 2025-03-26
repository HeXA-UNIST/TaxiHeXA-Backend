from datetime import datetime, timedelta
from flask import Blueprint, session, request
from src.utils import AuthManager, auth_required
from src.error import handle_exceptions
from src.schema import CreateTaxiInfoSchema, GetTaxiInfoSchema, TaxiParticipateTaxiSchema
from src.model import TaxiPool, PoolMember, User

taxi_router = Blueprint("taxi", __name__)
auth_manager = AuthManager(session)
create_taxi_info_schema = CreateTaxiInfoSchema()
get_taxi_info_schema = GetTaxiInfoSchema()
taxi_participate_taxi_schema = TaxiParticipateTaxiSchema()


@taxi_router.route("/create", methods=["POST"])
@handle_exceptions
@auth_required(auth_manager)
def create_taxi_info():
    data = request.get_json()
    create_taxi_info_schema.validate(data)
    data = create_taxi_info_schema.load(data)
    
    # TODO : nickname 제거하기 완
    creator_id = auth_manager.user_id
    new_pool = TaxiPool().create(**data, creator_id=creator_id)
    return {"taxi_id": new_pool.id, "room_id": new_pool.room_id}, 200


@taxi_router.route("/taxi_info", methods=["GET"])
@handle_exceptions
@auth_required(auth_manager)
def get_taxi_info():
    data = request.args
    get_taxi_info_schema.validate(data)
    data = get_taxi_info_schema.load(data)
    # TODO : 이거 고치기 완
    start_datetime = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    end_datetime = start_datetime + timedelta(days=1)
    # start_datetime = data.get("start_datetime")
    # end_datetime = data.get("end_datetime")
    
    taxi_pools = TaxiPool.select_taxi_pools_by_day(start_datetime, end_datetime) # List[TaxiPool]
    
    # TODO : nickname 가져오는 로직 추가해야함. 완완
    if len(taxi_pools) == 0:
        return {"msg": "팟이 없어요"}, 404
    

    result = {
        "taxi_list": [
            {
                **taxi_pool.as_dict(),
                "num_participation": PoolMember.count_pool_member(taxi_pool.id),
                "creator_nickname": User.select_by_id(id).nickname,
            }
            for taxi_pool in taxi_pools
        ]
    }
    return result, 200


@taxi_router.route("/participate", methods=["POST"])
@handle_exceptions
@auth_required(auth_manager)
def taxi_paticipate():
    data = request.get_json()
    taxi_participate_taxi_schema.validate(data)
    data = taxi_participate_taxi_schema.load(data)
    user_id = auth_manager.user_id
    taxi_id = data.get("taxi_id")
    PoolMember().create(taxi_id=taxi_id, user_id=user_id)
    taxi_pool = TaxiPool.select_taxi_pools_by_id(taxi_id)
    return {"taxi_id": taxi_id, "room_id": taxi_pool.room_id}, 200


@taxi_router.route("/participate", methods=["GET"])
@handle_exceptions
@auth_required(auth_manager)
def is_taxi_paticipate():
    data = request.args
    taxi_participate_taxi_schema.validate(data)
    data = taxi_participate_taxi_schema.load(data)
    user_id = auth_manager.user_id
    pool = PoolMember.select_pool_member_by_taxi_user_id(taxi_id=data.get("taxi_id"), user_id=user_id)
    return {"is_participated": True if pool else False}, 200
