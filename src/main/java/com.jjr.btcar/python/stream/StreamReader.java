package com.jjr.btcar.python.stream;

import java.io.IOException;
import java.io.InputStream;


//JRTODO maybe I shouldnt be using available(). read() might actually not block?
//http://stackoverflow.com/questions/11618662/system-in-available-call-gives-illegal-seek
public class StreamReader implements Runnable {

    private final InputStream in;
    private boolean kill = false;

    private enum RECORD_STATE {stopped, recording, stopping}
    private RECORD_STATE recording = RECORD_STATE.stopped;
    private StringBuffer record = new StringBuffer();
    private final DataLock dataNotifier;

    public StreamReader(InputStream in, DataLock dataNotifier) {
        this.in = in;
        this.dataNotifier = dataNotifier;
    }

    synchronized public void kill() {
        this.kill = true;
        notify();
    }

    @Override
    public void run () {
        kill = false;
        byte[] buffer = new byte[1024];
        int len;

        try {

            while(!kill) {
                synchronized (this) {
                    System.out.println("Reader going dormant.");
                    wait();
                }

                /*
                    While recording, recording all input while it's available. After someone calls
                    stopRecording(wait=true), we'll read the rest of the input before stopping. If
                    stopRecording(wait=false), we'll stop immediately. We'll wait() until the next start.
                */
                while(!isRecordingStopped()) {
                    while ( !kill
                            && !isRecordingStopped()
                            && (in.available() > 0)
                            && ( len = in.read(buffer)) > -1 ) {

                        //Store the incoming data first, otherwise it won't be available elsewhere
                        String string = new String(buffer, 0, len);
                        record.append(string);

                        //Notify when there be data
                        synchronized (dataNotifier) {
                            dataNotifier.setHasData(true);
                            dataNotifier.notifyAll();
                        }

                    }
                    if(recording == RECORD_STATE.stopping) {
                        recording = RECORD_STATE.stopped;
                        break;
                    } else {
                        Thread.sleep(50);
                    }
                }

            }

            System.out.println("ASYNC READER STOPPED. " + this);
        }
        catch ( IOException e ) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private boolean isRecordingStopped() {
        return recording == RECORD_STATE.stopped;
    }

    private boolean isRecording() {
        return recording == RECORD_STATE.recording;
    }

    synchronized public void startRecording() {
//        try {
            if(!isRecordingStopped()) {
                throw new IllegalStateException("Already recording input.");
            }

            //JRTODO how skip properly? just wind through it?
//            //Ignore anything before recording
//            if(in.available() > 0) {
//                in.skip(in.available());
//            }
            record.setLength(0);
            recording = RECORD_STATE.recording;

            notify();
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
    }

    /**
     *
     * @param wait Wait for stream to finish before returning. Otherwise, I'll just
     *             give you what I have.
     *
     *             Note, it doesn't always wait long enough.
     * @return
     */
    synchronized public String stopRecording(boolean wait) {

        if(wait) {
            recording = RECORD_STATE.stopping;

            //Wait for stream to stop.
            while (!isRecordingStopped()) {
                try {
                    Thread.sleep(50);
                    Thread.yield();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        } else {
            recording = RECORD_STATE.stopped;
        }

        return record.toString();
    }

}
