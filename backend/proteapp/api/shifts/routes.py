from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from proteapp.websockets import WSConnectionManager
from proteapp.api.shifts.schemas import ShiftAction, ShiftStatus, ShiftData
from proteapp.models.nosql.shift import Shift
from operator import attrgetter

router = APIRouter(tags=["shift"])

shift_ws_manager = WSConnectionManager()
status_ws_manager = WSConnectionManager()


@router.post("/shift/status", status_code=204)
async def post_status(request: Request, body: ShiftStatus):
    shift: Shift = request.app.state.shift
    shift.status = body.status

    await status_ws_manager.broadcast(ShiftStatus(status=shift.status).model_dump())


@router.websocket("/shift/status")
async def status_ws(websocket: WebSocket):
    shift: Shift = websocket.app.state.shift

    await status_ws_manager.connect(websocket)

    try:
        await status_ws_manager.send(ShiftStatus(status=shift.status).model_dump(), websocket)

        while True:
            await websocket.receive_json()

    except WebSocketDisconnect:
        status_ws_manager.disconnect(websocket)


@router.websocket("/shift")
async def websocket(websocket: WebSocket):
    shift: Shift = websocket.app.state.shift

    await shift_ws_manager.connect(websocket)

    try:
        await shift_ws_manager.broadcast(
            ShiftData(
                timetable=shift.timetable,
                connected=len(shift_ws_manager.active_connections),
            ).model_dump(),
        )

        while True:
            data = await websocket.receive_json()

            if shift.status == "closed":
                continue

            action = ShiftAction.model_validate(data)

            get_users = attrgetter(f"{action.shift.day}.{action.shift.time}")
            users: list[str] = get_users(shift.timetable)

            match action.type:
                case ShiftAction.ActionType.ADD_USER:
                    users.append(str(action.user))

                case ShiftAction.ActionType.REMOVE_USER:
                    users.remove(str(action.user))

            await shift_ws_manager.broadcast(
                ShiftData(
                    timetable=shift.timetable,
                    connected=len(shift_ws_manager.active_connections),
                ).model_dump(),
            )

            await shift.save()

    except WebSocketDisconnect:
        shift_ws_manager.disconnect(websocket)
        await shift_ws_manager.broadcast(
            ShiftData(
                timetable=shift.timetable,
                connected=len(shift_ws_manager.active_connections),
            ).model_dump(),
        )
