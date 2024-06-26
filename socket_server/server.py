# ---------------------------------------------------
# websockets to receive image and send message
# @author: Shi Junjie A178915
# Mon 10 June 2024
# ---------------------------------------------------

import os
import json
import asyncio
import websockets
import cv2
import time
from datetime import datetime

from .recg import process_image
# from backend_app.sql_handler import SQLHandler
from backend_app.app import sql_handler

# sql_handler = SQLHandler()
CLASS_DATE = '2024-06-15'
DEVICES = sql_handler.get_device(all=True)
DEVICES = {device.ip: device.location for device in DEVICES}
print(DEVICES)


async def receive_message(websocket, message_queue):
    """listen to message

    Args:
        websocket (_type_): _description_
        message_queue (_type_): _description_
    """
    async for message in websocket:
        # print('received message')
        await message_queue.put(message)

async def send_message(websocket, message_queue, image_queue, attendance_recorded, CLASSES):
    """send back message after image processed

    Args:
        websocket (_type_): _description_
        message_queue (_type_): _description_
        image_queue (_type_): _description_
    """
    receive_last_frame_time = 0.0
    process_last_frame_time = 0.0
    class_now = CLASSES[0]
    
    while True:
        message = await message_queue.get()
        
        # calculate receive time interval ------------------------------
        receive_time = time.time()
        receive_diff_time = receive_time - receive_last_frame_time
        receive_last_frame_time = receive_time
        if receive_diff_time == 0:
            receive_fps = '-1'
        else:
            receive_fps = round(1 / (receive_diff_time), 2)
        print('_______________')
        print('receive fps: {}'.format(receive_fps))
        # --------------------------------------------------------------
        
        image, processed_message, data = await process_image(message)
        msgs = json.load(processed_message)
            # attendance_recorded.append(image_info)
        # await image_queue.put(image_info)
        # print(processed_message)
        # print("----")
        # print()
        
        # check attendance
        if msgs['id'][0] != 'invalid':
            for i, student_id in enumerate(msgs['id']):
                
                # check liveness
                if not bool(msgs['live'][i]):
                    continue
                
                # locate the class now - for now we assume the first one
                # ignore

                # check if student in class
                classes_by_student = sql_handler.get_classes(
                    by='student_date', student_id=student_id, date=CLASS_DATE)
                class_ids_by_student = [class_.class_id for class_ in classes_by_student]
                
                if class_now.class_id not in class_ids_by_student:
                    # student not in class
                    continue
                
                # check if student in class time - ignore for now
                
                # chcek if student recorded
                if student_id in attendance_recorded:
                    print("{} already recorded".format(student_id))
                    continue
                else:
                    # record attendance
                    # demo
                    print("[Record Attendance]")
                    print(f"""
                        Course Code: {class_now.course_code}
                        Class ID: {class_now.class_id}
                        Student ID: {student_id}
                        Time Recorded: {datetime.now().strftime('%Y-%m-%d %H:%M')}
                        Attendance Status: present
                    """
                    )
                    print('--------------')

                    # # ignore for demo
                    # sql_handler.insert_attendance(
                    #     course_code=class_now.course_code,
                    #     class_id=class_now.class_id,
                    #     student_id=student_id,
                    #     record_time=datetime.now(),
                    #     status='present'        # assume 'present' for simplicity
                    # )
                    
                    # append to attendance_recorded
                    attendance_recorded.append(student_id)

                    # only send message if student record for the first time
                    await websocket.send(processed_message)

                    # store the message for visualisation
                    image_info = [image, processed_message, data]
                    await image_queue.put(image_info)

        message_queue.task_done()

        # calculate processing time interval ------------------------------
        process_time = time.time()
        process_diff_time = process_time - process_last_frame_time
        process_last_frame_time = process_time
        if process_diff_time == 0:
            process_fps = '-1'
        else:
            process_fps = round(1 / (process_diff_time), 2)
        print('total process fps: {}'.format(process_fps))
        # --------------------------------------------------------------

async def show_stream(image_queue):
    """store image processed to a dir

    Args:
        image_queue (_type_): _description_
    """
    stream_image_dir = "/home/junja/attendance_system_backend/stream"       # change to the dir where u want to place the processed image
    stream_idx = 0
    while True:
        img, msg, data = await image_queue.get()
        msg_dict = json.loads(msg)
        # cv2 visualise ---------------------------------------------------------
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # print(data)
        try:
            if msg_dict['id'][0] != "invalid":
                box_color = (0, 0, 225)
                if msg_dict['live'][0] == 'True':
                    box_color = (0, 255, 0)

                cv2.rectangle(
                    img, (data["bboxes"][0][0], data["bboxes"][0][1]),
                    (data["bboxes"][0][2], data["bboxes"][0][3]), box_color, 2,
                )
            
                cv2.putText(img, msg_dict['id'][0], (20, 20), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
                cv2.putText(
                    img, 'live: {} {:.3f}'.format(msg_dict['live'][0], data['liveness_scores'][0]), (20, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
                
        except:
            cv2.putText(img, 'Exception', (20, 100), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)

        img_file_name = 'stream_{}.jpg'.format(stream_idx)
        cv2.imwrite(os.path.join(
            stream_image_dir, img_file_name
            ), img)
        stream_idx += 1
        image_queue.task_done()

async def websocket_handler(websocket, path):
    """websocket handler

    Args:
        websocket (_type_): _description_
        path (_type_): _description_
    """
    client_ip, _ = websocket.remote_address
    print('[Client Connected] IP: {},'.format(client_ip))
    if client_ip in list(DEVICES.keys()):
        print(' - device location: {}'.format(DEVICES[client_ip]))
    else:
        print(' - device not found!')
        return

    attendance_recorded = []
    CLASSES = sql_handler.get_classes(by='location_date', location=DEVICES[client_ip], date=CLASS_DATE)

    message_queue = asyncio.Queue()
    image_queue = asyncio.Queue()

    receive_task = asyncio.create_task(receive_message(websocket, message_queue))
    send_task = asyncio.create_task(send_message(websocket, message_queue, image_queue, attendance_recorded, CLASSES))
    show_stream_task = asyncio.create_task(show_stream(image_queue))
    
    await asyncio.gather(
        receive_task,
        send_task,
        show_stream_task,
    )

async def start_socket_server(port):
    """start websocket server

    Args:
        port (_type_): _description_
    """
    print('running websocket server on port: {}'.format(port))
    server = await websockets.serve(websocket_handler, '0.0.0.0', port)
    await server.wait_closed()
    
def run_socket_server(port):
    asyncio.run(start_socket_server(port))

# run_socket_server(5000)