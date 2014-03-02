package com.jjr.btcar.serial;

import com.jjr.btcar.python.stream.StreamReader;

public interface ISerial {

    public void connect(String device, int baud);

    /**
     * Send command and wait for the reply.
     * @param command
     * @return
     */
    public String sendCommand(String command);

    public void sendBlind(String command);

    public StreamReader sendAsyncCommand(String command) ;

    public void disconnect();

}
