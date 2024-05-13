from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO(model=r"D:\tmp\yolov8\runs\detect\train3\weights\best.pt")
    model.train(data='D:/.dataset/overwatch/ow.yaml', epochs=20, imgsz=640)
