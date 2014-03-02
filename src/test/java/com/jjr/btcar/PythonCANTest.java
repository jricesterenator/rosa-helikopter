package com.jjr.btcar;

import com.jjr.btcar.serial.SerialPython;
import org.junit.Test;

public class PythonCANTest {

    @Test
    public void testName() throws Exception {
        SerialPython sp = new SerialPython("btcar.py");//JRTODO pass in
        sp.connect("device", 9600);

        PythonCAN can = new PythonCAN(sp);
        can.sendATMA();

        Thread.sleep(3000);

        String output = can.stopATMA();
        System.out.println(">>>>>" + output);

        Thread.sleep(1000);

        sp.disconnect();

    }
}
