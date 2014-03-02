package com.jjr.btcar.reader3;

import java.util.List;

public class PythonCommandHandler {

    private final Process process;
    private PythonStreamReader3 streamReader;
    private PythonStreamWriter pythonStreamWriter;

    private List<String> commands;
    private List<PythonOutput> output;

    private Object pythonLoadedLock = new Object();
    private Object pythonCommandLock = new Object();

    private volatile boolean commandComplete;
    private PythonOutput asyncOut;

    public PythonCommandHandler(Process process) {
        this.process = process;

        streamReader = new PythonStreamReader3(process.getInputStream()) {
            @Override
            protected void onPythonLoaded() {
                synchronized (pythonLoadedLock) {
                    pythonLoadedLock.notifyAll();
                }
            }

            @Override
            protected void onCommandComplete() {
                synchronized (pythonCommandLock) {
                    commandComplete = true;
                    if(asyncRunning) {
                        asyncRunning = false;
                    }
                }
            }
        };
        new Thread(streamReader).start();

        pythonStreamWriter = new PythonStreamWriter(process.getOutputStream());
        new Thread(pythonStreamWriter).start();

        commands = pythonStreamWriter.getCommands();
        output = streamReader.getCommandOutput();
    }

    public String sendCommand(String string) {
        commandComplete = false;

        if(!string.endsWith("\n")) {
            string += '\n';
        }

        int nextCommandIndex = commands.size();

        pythonStreamWriter.write(string);

        System.out.print(">>> " + string);

        while (!commandComplete) {
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        PythonOutput pyoutput = this.output.get(nextCommandIndex);
        if(pyoutput.isLive()) {
            System.out.println("Something's wrong, output shouldn't be live now.");
        }

        return pyoutput.getString();
    }

    private volatile boolean asyncRunning = false;
    public void sendAsyncCommand(String string) {

        if(!string.endsWith("\n")) {
            string += '\n';
        }

        if(asyncRunning) {
            System.out.println("Async already running, output will continue to be" +
                    " captured under the original async command.");
        } else {
            asyncOut = output.get(output.size()-1);
        }

        asyncRunning = true;
        pythonStreamWriter.write(string);
        System.out.print("... " + string);

    }

    public PythonOutput waitForAsyncToFinish() {
        while (asyncRunning) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        return asyncOut;
    }

    public void dumpCommands() {

        for(int i=0; i< commands.size(); ++i) {
            System.out.print(">>> " + commands.get(i));
            System.out.print(output.get(i).getString());

        }

    }

    public void waitUntilLoaded() {
        synchronized (pythonLoadedLock) {
            try {
                pythonLoadedLock.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

}
