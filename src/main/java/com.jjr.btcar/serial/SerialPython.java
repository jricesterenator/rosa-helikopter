package com.jjr.btcar.serial;

import com.jjr.btcar.python.PythonProcess;
import com.jjr.btcar.python.stream.StreamReader;

public class SerialPython extends PythonProcess implements ISerial {

    public SerialPython(String filename) {
        super(filename);
    }

    public void connect(String device, int baud) {
        executeInteractively();

        execute(String.format(
                "connect('%s', '%d')", device, baud
        ));
    }

    @Override
    public String sendCommand(String command) {

        String output = execute(String.format(
                "write('%s')", command
        ));

        return output;

    }

    @Override
    public StreamReader sendAsyncCommand(String command) {
        return executeAsync(String.format(
                "write('%s')", command
        ));
    }

    @Override
    public void disconnect() {
        terminate();
    }
}

