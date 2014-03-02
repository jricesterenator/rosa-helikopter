package com.jjr.btcar.reader3;

import java.io.IOException;

public class PythonProcess3 {

    private final String filename;
    private Process process;
    private PythonCommandHandler commandHandler;

    public PythonProcess3(String filename) {
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

    public void executeInteractively() throws InterruptedException {
        if(process != null) {
            throw new IllegalStateException("Process is already active.");
        }

        try {

            ProcessBuilder builder;
            if(filename != null) {
                builder = new ProcessBuilder("python", "-i", filename);
            } else {
                builder = new ProcessBuilder("python", "-i");
            }
            builder.redirectErrorStream(true);
            process = builder.start();

            commandHandler = new PythonCommandHandler(process);
            commandHandler.waitUntilLoaded();
            System.out.println("Python is ready.");

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public String sendCommand(String string) {
        String output = commandHandler.sendCommand(string);
        System.out.print("#" + output);
        return output;
    }

    public void sendAsyncCommand(String string) {
        commandHandler.sendAsyncCommand(string);
    }

    public PythonOutput waitForAsyncToFinish() {
        return commandHandler.waitForAsyncToFinish();
    }
}

