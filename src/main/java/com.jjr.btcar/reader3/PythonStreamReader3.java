package com.jjr.btcar.reader3;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PythonStreamReader3 implements Runnable {

    private List<PythonOutput> commandOutput = Collections.synchronizedList(new ArrayList<PythonOutput>());

    private final InputStream in;
    private boolean kill = false;

    public PythonStreamReader3(InputStream inputStream) {
        this.in = inputStream;
    }

    @Override
    public void run() {
        int len;
        byte[] buffer = new byte[1024];

        PythonOutput pythonOutput = new PythonOutput(new StringBuffer());
        commandOutput.add(pythonOutput);

        while(!kill) {

            try {

                while(( len = this.in.read(buffer)) > -1) {
                    String string = new String(buffer, 0, len);

                    int prevIndex = 0;
                    int promptIndex;
                    while( (promptIndex = getPromptIndex(string, prevIndex)) > -1 ) {

                        StringBuffer sb = pythonOutput.getStringBuffer();
                        sb.append(string.substring(prevIndex, promptIndex));
                        pythonOutput.setLive(false);

                        if(isPythonFirstLoaded()) {
                            onPythonLoaded();
                        } else {
                            onCommandComplete();
                        }
                        pythonOutput = new PythonOutput(new StringBuffer());
                        commandOutput.add(pythonOutput);

                        prevIndex = promptIndex + 4;
                    }
                    if(prevIndex < string.length()) {
                        StringBuffer sb = pythonOutput.getStringBuffer();
                        sb.append(string.substring(prevIndex));
                    }

                }

            } catch (IOException e) {
                e.printStackTrace();
            }

            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * If '...' becomes an issue, I don't really need to support multi-line python commands
     * @param string
     * @param prevIndex
     * @return
     */
    private int getPromptIndex(String string, int prevIndex) {
        int promptIndex = string.indexOf(">>> ", prevIndex);
//        if(promptIndex == -1) {
//            promptIndex = string.indexOf("... ", prevIndex);
//        }
        return promptIndex;
    }

    /**
     * Python is 'first loaded' when the first output is completely recorded.
     * @return
     */
    private boolean isPythonFirstLoaded() {
        return commandOutput.size() == 1 && !commandOutput.get(0).isLive();
    }

    /**
     * Override this if you want to be notified when a command command is complete.
     */
    protected void onCommandComplete() {
        ;;;
    }

    /**
     * Override this if you want to be notified when Python is finished loading.
     */
    protected void onPythonLoaded() {
        ;;;
    }

    public void kill() {
        kill = true;
    }

    public List<PythonOutput> getCommandOutput() {
        return commandOutput;
    }
}

class PythonOutput {

    private StringBuffer sb;
    private volatile boolean live;

    public PythonOutput(StringBuffer sb) {
        this.sb = sb;
        this.live = true;
    }

    public StringBuffer getStringBuffer() {
        return sb;
    }

    public String getString() {
        return sb.toString();
    }

    public boolean isLive() {
        return live;
    }

    public void setLive(boolean live) {
        this.live = live;
    }
}
