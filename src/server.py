import cv2
from flask import Flask, render_template, Response, request
from camera import Camera
from motors_controller import MotorsController

controller = MotorsController(left_motor_gpios=('GPIO26', 'GPIO19'),
                              right_motor_gpios=('GPIO21', 'GPIO20'))
camera = Camera()

class Server:
    app = Flask(__name__)

    @classmethod
    def run(cls):
        cls.app.run(debug=False, use_reloader=False, host="0.0.0.0")

    @staticmethod
    @app.route('/')
    def index():
        return render_template('index.html')

    @staticmethod
    @app.route('/update_engines_usage_slider', methods=['POST'])
    def update_engines_usage_slider():
        data = request.get_json()
        engines_usage = int(data['value'])
        
        controller.set_engines_usage_from_slider(engines_usage)
        
        speeds = controller.get_motors_speed()
        print(f"A: {speeds[0]}\nB: {speeds[1]}")
        return 'Slider value received'

    @staticmethod
    @app.route('/update_balance_slider', methods=['POST'])
    def update_balance_slider():
        data = request.get_json()
        balance = int(data['value'])
        
        controller.set_balance_from_slider(balance)
        
        return 'Slider value received'
    
    @staticmethod
    @app.route('/adjust_quality_slider', methods=['POST'])
    def adjust_quality_slider():
        data = request.get_json()
        quality = int(data['value'])
        
        camera.set_compression(quality)
        
        return 'Slider value received'

    @app.route('/video_feed')
    def video_feed():
        return Response(Server.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @staticmethod
    def generate_frames():
        while True:
            """#==========OPENCV WEBP==========
            # frame = camera.get_frame()
            # print(f"Encode start: {time()}")
            # _, webp_image = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, quality])
            # frame_bytes = webp_image.tobytes()
            # print(f"Encode end: {time()}\n\n")
            # RESULTS:
             
             
              #==========PIL WEBP==========
            # frame = Image.fromarray(camera.get_frame()).convert('RGB')
            # print(f"Encode start: {time()}")
            # output = BytesIO()
            # frame.save(output, format='webp', quality=quality)
            # frame_bytes = output.getvalue()
            # print(f"Encode end: {time()}\n\n")
            # RESULTS:
            
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/webp\r\n\r\n' + frame_bytes + b'\r\n\r\n')
            

            # # #==========OPENCV JPEG==========
            #frame = camera.get_frame()
           # print(f"Encode start: {time()}")
            #_, jpeg_image = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            #frame_bytes = jpeg_image.tobytes()
            #print(f"Encode end: {time()}\n\n")
             # RESULTS:

           

            # #==========PIL JPEG=========="""
            
           
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + camera.get_jpeg_bytes() + b'\r\n\r\n')
            
          