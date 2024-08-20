from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    HTTPException,
    Depends,
)
from proteapp.websockets import WSConnectionManager
from proteapp.api.shifts.schemas import ShiftAction, ShiftStatus, ShiftData
from proteapp.models.nosql.shift import Shift
from operator import attrgetter
from ulid import ULID
from proteapp.api.deps import get_logged_user_http, get_logged_user_ws

router = APIRouter(tags=["shift"])

shift_ws_manager = WSConnectionManager()
status_ws_manager = WSConnectionManager()


@router.post("/shift/status", status_code=204, dependencies=[Depends(get_logged_user_http)])
async def post_status(body: ShiftStatus):
    shift = await Shift.find_one()

    if not shift:
        raise HTTPException(500, "Shift could not be found")

    shift.status = body.status
    await shift.save()

    await status_ws_manager.broadcast(ShiftStatus(status=shift.status).model_dump())


@router.websocket("/shift/status", dependencies=[Depends(get_logged_user_ws)])
async def status_ws(websocket: WebSocket):
    await status_ws_manager.connect(websocket)

    shift = await Shift.find_one()

    if not shift:
        shift_ws_manager.disconnect(websocket)
        raise WebSocketException(1011, "Shift could not be found")

    try:
        await status_ws_manager.send(ShiftStatus(status=shift.status).model_dump(), websocket)

        while True:
            await websocket.receive_json()

    except WebSocketDisconnect:
        status_ws_manager.disconnect(websocket)


@router.websocket("/shift", dependencies=[Depends(get_logged_user_ws)])
async def websocket(websocket: WebSocket):
    await shift_ws_manager.connect(websocket)

    shift = await Shift.find_one()

    if not shift:
        shift_ws_manager.disconnect(websocket)
        raise WebSocketException(1011, "Shift could not be found")

    try:
        await shift_ws_manager.broadcast(
            ShiftData(
                timetable=shift.timetable,
                connected=len(shift_ws_manager.active_connections),
            ).model_dump(),
        )

        while True:
            data = await websocket.receive_json()

            shift = await Shift.find_one()

            if not shift:
                shift_ws_manager.disconnect(websocket)
                raise WebSocketException(1011, "Shift could not be found")

            if shift.status == "closed":
                continue

            action = ShiftAction.model_validate(data)

            get_users = attrgetter(f"{action.shift.day}.{action.shift.time}")
            users: list[ULID] = get_users(shift.timetable)

            match action.type:
                case ShiftAction.ActionType.ADD_USER:
                    users.append(action.user)

                case ShiftAction.ActionType.REMOVE_USER:
                    users.remove(action.user)

            await shift.save()

            await shift_ws_manager.broadcast(
                ShiftData(
                    timetable=shift.timetable,
                    connected=len(shift_ws_manager.active_connections),
                ).model_dump(),
            )

    except WebSocketDisconnect:
        shift_ws_manager.disconnect(websocket)

        shift = await Shift.find_one()

        if shift:
            await shift_ws_manager.broadcast(
                ShiftData(
                    timetable=shift.timetable,
                    connected=len(shift_ws_manager.active_connections),
                ).model_dump(),
            )
