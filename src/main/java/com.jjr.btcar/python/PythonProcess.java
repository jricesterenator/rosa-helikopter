package com.jjr.btcar.python;

import com.jjr.btcar.python.stream.DataLock;
import com.jjr.btcar.python.stream.ErrorStreamReader;
import com.jjr.btcar.python.stream.StreamReader;
import com.jjr.btcar.python.stream.StreamWriter;

import java.io.IOException;

public class PythonProcess {

    private final String filename;

    private Process process;

    private StreamWriter stdinWriter;
    private StreamReader stdoutReader;
    private ErrorStreamReader stderrReader;

    private Thread stderrThread;
    private Thread stdinThread;
    private Thread stdoutThread;
    private final DataLock dataNotifier = new DataLock();

    public PythonProcess(String filename) {
        this.filename = filename;

        Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("SHUTDOWN HOOK!");
                if(process != null) {
                    System.out.println("Terminating python process.");
                    process.destroy();
                }
            }
        }));

    }

    public void executeInteractively() {
        final Object startupLock = new Object();

        if(process != null) {
            throw new IllegalStateException("Process is already active.");
        }

        try {

            Runtime r = Runtime.getRuntime();
            process = r.exec("python -i " + filename);

            //Error stream reader. Just spews everything.
            stderrReader = new ErrorStreamReader(PythonProcess.this.process.getErrorStream(), dataNotifier) {
                @Override
                protected void onPythonReady() {
                    synchronized (startupLock) {
                        System.out.println("Python is ready.");
                        startupLock.notify();
                    }
                }
            };
            stderrThread = newDaemonThread(stderrReader);
            stderrThread.start();

            //This allows us to write to the python program's stdin
            stdinWriter = new StreamWriter(this.process.getOutputStream());
            stdinThread = newDaemonThread(stdinWriter);
            stdinThread.start();

            //This allows us to selectively read the python program's stdout
            stdoutReader = new StreamReader(this.process.getInputStream(), dataNotifier);
            stdoutThread = newDaemonThread(stdoutReader);
            stdoutThread.start();

            //Wait for python startup notification from the error stream reader
            synchronized (startupLock) {
                try {
                    System.out.println("Waiting for python to start up.");
                    startupLock.wait();
                    System.out.println("Good to go!");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public String execute(String command) {

        dataNotifier.setHasData(false);
        stdoutReader.startRecording();

        //Send command to python program
        stdinWriter.write(command + "\n");

        synchronized (dataNotifier) {
            try {
                if(!dataNotifier.isHasData()) {
//                    System.out.println("WAITING FOR DATA");
                    dataNotifier.wait();
//                    System.out.println("FOUND DATA");
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        String output = stdoutReader.stopRecording(true);
        System.out.println("Recorded this output: " + output);

        return output;

    }

    public void sendBlind(String command) {

        //Send command to python program
        stdinWriter.write(command + "\n");
    }

    public StreamReader executeAsync(String command) {

        dataNotifier.setHasData(false);
        stdoutReader.startRecording();

        //Send command to python program
        stdinWriter.write(command + "\n");

        synchronized (dataNotifier) {
            try {
                if(!dataNotifier.isHasData()) {
//                    System.out.println("WAITING FOR DATA");
                    dataNotifier.wait();
//                    System.out.println("FOUND DATA");
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        //JRTODO issue a stop token or something
        return stdoutReader;

    }

    public void terminate() {
        System.out.println("Terminating python process and stream readers.");
        process.destroy();
        process = null;

        stdinWriter.kill();
        stderrReader.kill();
        stdoutReader.kill();

        awaitTermination(stdinThread);
        awaitTermination(stdoutThread);
        awaitTermination(stderrThread);
    }

    private void awaitTermination(Thread thread) {
        while(thread.isAlive()) {
            try {
                Thread.sleep(10);
                Thread.yield();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    private Thread newDaemonThread(Runnable runnable) {
        Thread thread = new Thread(runnable);
        thread.setDaemon(true);
        return thread;
    }

}

