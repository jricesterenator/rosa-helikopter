package com.jjr.btcar.reader3;

import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PythonStreamWriter implements Runnable
{
    private final OutputStream out;
    private boolean kill = false;
    private List<String> commands = Collections.synchronizedList(new ArrayList<String>());

    public PythonStreamWriter(OutputStream out) {
        this.out = out;
        commands.add("__init__\n");
    }

    synchronized public void run ()
    {
        kill = false;

        while(!kill) {
            try {
                wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        System.out.println("Stream writer thread done.");
    }

    public void write(String string) {

        try {
            System.out.println("WRITING: " + string.trim());

            out.write(string.getBytes());
            out.flush();

            commands.add(string);

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    synchronized public void kill() {
        kill = true;
        notify();
    }

    public List<String> getCommands() {
        return commands;
    }
}
