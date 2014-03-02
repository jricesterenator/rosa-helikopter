//package com.jjr.btcar.p2.stream.pythonstreams;
//
//import DataLock;
//
//import java.io.IOException;
//import java.io.InputStream;
//
//public class PythonStreamReader implements Runnable {
//
//    private final InputStream in;
//    private boolean kill = false;
//
//    private enum RECORD_STATE {stopped, recording, stopping}
//    private RECORD_STATE recording = RECORD_STATE.stopped;
//    private StringBuffer record = new StringBuffer();
//    private final DataLock dataNotifier;
//
//    private boolean pythonReady = false;
//
//    public PythonStreamReader(InputStream in, DataLock dataNotifier) {
//        this.in = in;
//        this.dataNotifier = dataNotifier;
//    }
//
//    synchronized public void kill() {
//        this.kill = true;
//        notify();
//    }
//
//    @Override
//    public void run () {
//        kill = false;
//        byte[] buffer = new byte[1024];
//        int len;
//
//        try {
//
//            while(!kill) {
//                if(pythonReady) {
//                    synchronized (this) {
//                        System.out.println("Stream wait.");
//                        wait();
//                    }
//                }
//
//                /*
//                    While recording, recording all input while it's available. After someone calls
//                    stopRecording(wait=true), we'll read the rest of the input before stopping. If
//                    stopRecording(wait=false), we'll stop immediately. We'll wait() until the next start.
//                */
//                while(!pythonReady || !isRecordingStopped()) {
//                    while ( (!pythonReady || (!kill && !isRecordingStopped()))
//                            && (in.available() > 0)
//                            && ( len = in.read(buffer)) > -1 ) {
//
//                        String string = new String(buffer, 0, len);
//
//                        if(string.contains(">>> ")) {
//                            if(!pythonReady) {
//                                pythonReady = true;
//                                onPythonReady();
//                            } else {
//                                if(string.endsWith(">>> ") && !isRecordingStopped()) {
//                                    recording = RECORD_STATE.stopped;
//                                }
//                            }
//                        }
//
//                        string = string.replace(">>> ", "");
//                        record.append(string);
//
//                        //Notify when there be data
//                        synchronized (dataNotifier) {
//                            dataNotifier.setHasData(true);
//                            dataNotifier.notifyAll();
//                        }
//
//
//                    }
//                    if(recording == RECORD_STATE.stopping) {
//                        recording = RECORD_STATE.stopped;
//                        break;
//                    } else {
//                        Thread.sleep(50);
//                    }
//                }
//
//            }
//
//            System.out.println("ASYNC READER STOPPED. " + this);
//        }
//        catch ( IOException e ) {
//            e.printStackTrace();
//        } catch (InterruptedException e) {
//            e.printStackTrace();
//        }
//    }
//
//    private boolean isRecordingStopped() {
//        return recording == RECORD_STATE.stopped;
//    }
//
//    private boolean isRecording() {
//        return recording == RECORD_STATE.recording;
//    }
//
//    synchronized public void startRecording() {
//        try {
//            if(!isRecordingStopped()) {
//                throw new IllegalStateException("Already recording input.");
//            }
//
//            //Ignore anything before recording
//            if(in.available() > 0) {
//                in.skip(in.available());
//            }
//            record.setLength(0);
//            recording = RECORD_STATE.recording;
//
//            notify();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//    }
//
//    /**
//     * @return
//     */
//    synchronized public String stopRecordingWait() {
//        //Wait for stream to stop.
//        while (!isRecordingStopped()) {
//            try {
//                Thread.sleep(50);
//                Thread.yield();
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
//        }
//        return record.toString();
//    }
//
//    synchronized public String stopRecordingNow() {
//        recording = RECORD_STATE.stopped;
//        return record.toString();
//    }
//
//    synchronized public String stopRecordingAtStreamEnd() {
//        recording = RECORD_STATE.stopping;
//        //Wait for stream to stop.
//        while (!isRecordingStopped()) {
//            try {
//                Thread.sleep(50);
//                Thread.yield();
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
//        }
//        return record.toString();
//    }
//
//
//    /**
//     * Called when the first set of ">>>" appears, meaning python is started.
//     * Override to get the notification.
//     */
//    protected void onPythonReady() {
//        ;;;
//    }
//
//}
