from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from proteapp.websockets import WSConnectionManager
from proteapp.api.shifts.schemas import ShiftAction, ShiftActionType, ShiftStatus
from proteapp.models.nosql.shift import Shift
from operator import attrgetter

router = APIRouter(prefix="/shift", tags=["shift"])

shift_ws_manager = WSConnectionManager()
status_ws_manager = WSConnectionManager()


@router.post("/status", status_code=204)
async def post_status(request: Request, body: ShiftStatus):
    shift: Shift = request.app.state.shift
    shift.status = body.status

    await status_ws_manager.broadcast(ShiftStatus(status=shift.status).model_dump())


@router.websocket("/status")
async def status_ws(websocket: WebSocket):
    shift: Shift = websocket.app.state.shift

    await status_ws_manager.connect(websocket)

    try:
        await status_ws_manager.send(ShiftStatus(status=shift.status).model_dump(), websocket)

        while True:
            await websocket.receive_json()

    except WebSocketDisconnect:
        status_ws_manager.disconnect(websocket)


@router.websocket("/")
async def websocket(websocket: WebSocket):
    # TODO: Save shift on DB
    shift: Shift = websocket.app.state.shift

    await shift_ws_manager.connect(websocket)

    try:
        await shift_ws_manager.send(shift.timetable.model_dump(), websocket)

        while True:
            data = await websocket.receive_json()

            if shift.status == "closed":
                continue

            action = ShiftAction.model_validate(data)

            get_users = attrgetter(f"{action.shift.day}.{action.shift.time}")
            users: list[str] = get_users(shift.timetable)

            match action.type:
                case ShiftActionType.ADD_USER:
                    users.append(str(action.user))

                case ShiftActionType.REMOVE_USER:
                    users.remove(str(action.user))

            await shift_ws_manager.broadcast(shift.timetable.model_dump())

    except WebSocketDisconnect:
        shift_ws_manager.disconnect(websocket)
