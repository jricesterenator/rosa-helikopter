//package com.jjr.btcar;
//
//import com.jjr.btcar.p2.stream.AsyncStreamReader;
//
//public class Controller {
//
//    private Results results;
//    private ISerial serial;
//    private AsyncStreamReader atma;
//
//    enum State { stopped, baseline, recording;}
//
//    private State state = State.stopped;
//
//    public void connect(String device, int baud) {
//        serial = new SerialPython("btcar.py");
//        serial.connect(device, baud);
//        serial.write("ATL1"); //set line endings to \n
//    }
//
//    public boolean verifyConnection() {
//        String reply = serial.write("ATSP0");
//        return "Ok".equals(reply.trim());
//    }
//
//    public void disconnect() {
//        serial.disconnect();
//    }
//
//    public void newSession() {
//        results = new Results();
//        state = State.stopped;
//    }
//
//    public void startRecording() {
//        //ATMA - all data goes to currentBaseline
//        state = State.baseline;
//
//        atma = serial.sendAsyncCommand("ATMA");
//    }
//
//    public void markBefore() {
//        //-switch ATMA data to going into currentRecording
//        state = State.recording;
//
//        atma.getOutput().append("\n################ BEGIN RECORDING #################\n");
//    }
//
//    public void stopRecording() {
//        state = State.stopped;
//
//        //Stop the output listener send a newline to kill the ATMA command
//        serial.write("");
////        AsyncStreamReader asyncStop = serial.sendAsyncCommand("");
//        atma.kill();
////        asyncStop.kill();
//
//        while (atma.getParentThread().isAlive()) {
//            Thread.yield();
//        }
//    }
//
//    public void saveRun() {
//        results.saveRun(atma.getOutput().toString());
//        atma = null;
//    }
//
//    public Results getSessionData() {
//        return results;
//    }
//}
