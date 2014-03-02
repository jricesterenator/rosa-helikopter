package com.jjr.btcar.python.stream;

import java.io.IOException;
import java.io.OutputStream;

public class StreamWriter implements Runnable
{
    private final OutputStream out;
    private boolean kill = false;

    public StreamWriter(OutputStream out) {
        this.out = out;
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

        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    synchronized public void kill() {
        kill = true;
        notify();
    }

}
