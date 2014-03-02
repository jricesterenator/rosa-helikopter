package com.jjr.btcar.python.stream;

import org.apache.commons.lang.StringUtils;

import java.io.IOException;
import java.io.InputStream;

public class ErrorStreamReader implements Runnable
{
    private final InputStream in;
    private boolean kill = false;
    private boolean pythonReady = false;
    private final DataLock dataNotifier;

    public ErrorStreamReader(InputStream in, DataLock dataNotifier) {
        this.in = in;
        this.dataNotifier = dataNotifier;
    }

    public void kill() {
        kill = true;
    }

    public void run () {
        byte[] buffer = new byte[1024];
        int len;
        try
        {
            while(!kill) {
                while (!kill && ( len = this.in.read(buffer)) > -1)
                {
                    String rawString = new String(buffer, 0, len);

                    if(StringUtils.isNotBlank(rawString)) {
                        synchronized (dataNotifier) {
                            dataNotifier.setHasData(true);
                            dataNotifier.notifyAll();
                        }
                        printErrorText(rawString);
                    }

                    //Notify when python is ready for the first time.
                    if(!pythonReady && rawString.contains(">>>")) {
                        pythonReady = true;
                        onPythonReady();
                    }
                }
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("Error stream thread done. " + this);
    }

    private void printErrorText(String rawString) {
        String string = rawString.replace(">>> ", "");
        string = string.trim();
        string = string.replace("\n", "\n[ERROR] ");
        System.out.println("[ERROR] " + string);
    }

    /**
     * Called when the first set of ">>>" appears, meaning python is started.
     * Override to get the notification.
     */
    protected void onPythonReady() {
        ;;;
    }
}
