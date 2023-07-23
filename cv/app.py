# 导入必要的库
import cv2
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from color import ColorDetection

# 初始化Flask应用和数据库
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///colors.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# 创建数据库模型
class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Color {self.color_name}>"
        

# 路由和视图函数
@app.route('/')
def index():
    colors = Color.query.all()
    return render_template('index.html', colors=colors)

# 查询数据库内容
@socketio.on('query_colors_by_color_name', namespace='/')
def query_colors_by_color_name(colorName):
    colors = Color.query.filter_by(color_name=colorName).all()
    color_data = [{'id': color.id, 'color_name': color.color_name} for color in colors]
    emit('query_result', color_data)

# 删除颜色记录
@socketio.on('delete_color', namespace='/')
def delete_color(colorName):
    color = Color.query.filter_by(color_name=colorName).first()
    if color:
        db.session.delete(color)
        db.session.commit()
        emit('color_deleted', colorName)

# ...

# 颜色识别逻辑，注意：此处只执行一次识别，并非循环执行
def recognize_color_once(frame):
    detect = 40  # 將此值替換為您期望的偵測百分比
    resize = 60  # 將此值替換為您期望的調整大小百分比
    debugMode = 'n'  # 設置為 'y' 以啟用除錯模式，'n' 以禁用
    c = ColorDetection(frame, detect, resize, debugMode)  # 将帧直接传递给 ColorDetection 类
    color_result = c.main()
    # 在这里实现您的颜色识别算法
    # 返回颜色名称
    return color_result  # 示例颜色

# 主要逻辑
if __name__ == '__main__':
    with app.app_context():  # 创建应用上下文
        db.create_all()  # 创建数据库表

    cap = cv2.VideoCapture(0)  # 打开摄像头
    while True:
        ret, frame = cap.read()
        cv2.imshow('Frame', frame)

        # 颜色识别逻辑仅在按下 "esc" 键时执行一次
        if cv2.waitKey(1) & 0xFF == 27:  # 按下"esc"键
            color = recognize_color_once(frame)
            print(f"The dominant color is {color}.")
            # 将颜色信息保存到数据库
            with app.app_context():  # 使用应用上下文
                db.session.add(Color(color_name=color))
                db.session.commit()

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按下"q"键退出
            break

    cap.release()
    cv2.destroyAllWindows()

    app.run()  # 启动Flask应用
