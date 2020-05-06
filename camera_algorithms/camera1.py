from camera_algorithms.camera1_model import PeopleDetector
#Loading  model
net = PeopleDetector()
net.load_network()
# Get the video writer initialized to save the output video
def queue (img) :
    # get frame from the video
    frame=img
    #Get te predictions from the model 
    outs = net.predict(frame)
    #Use model predictions to get total numbers of persons in the queue and number of persons in danger
    _,n_total,n_mal=net.process_preds(frame, outs)
    net.clear_preds()
    return frame,n_total,n_mal