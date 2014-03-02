package com.jjr.btcar;

import com.jjr.btcar.python.stream.StreamReader;
import com.jjr.btcar.serial.ISerial;

//JRTODO this really shouldnt be python or stream implementation specific..
public class PythonCAN {

    private final ISerial
            serial;

    private String currentCommand = null;
    private StreamReader asyncReader;

    public PythonCAN(ISerial serial) {
        this.serial = serial;
    }

    public void sendATMA() {
        currentCommand = "ATMA";
        asyncReader = serial.sendAsyncCommand("ATMA");//JRTODO make a token
    }

    public String stopATMA() {
        if(!"ATMA".equals(currentCommand)) {
            throw new IllegalStateException("ATMA command not active.");
        }

        sendBlank();
        String output = asyncReader.stopRecording(false);

        currentCommand = null;
        asyncReader = null;

        return output;
    }

    private void sendBlank() {
        serial.sendBlind("");
    }
}
